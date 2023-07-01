import axios from 'axios';
import moment from 'moment';
import express from 'express';

const walletAddress = 'TPjereztht2j6Ffq3vGyMGwvNvKErVNYuv';
const contractAddress = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t';

const app = express();

app.get('/fetch-transactions', (req, res) => {
    const now = moment();
    const time = now.clone().subtract(5, 'minutes');

    const fetchTransactions = (url, direction) => {
        return axios.get(url)
            .then(response => {
                const transactions = response.data.data;
                return transactions.map(tx => {
                    const date = moment(tx.block_timestamp).format('YYYY-MM-DD HH:mm:ss');
                    const amount = tx.value / (10 ** 6);
                    return {
                        date: date,
                        direction: direction,
                        amount: amount
                    };
                });
            });
    };

    const outgoingUrl = `https://api.trongrid.io/v1/accounts/${walletAddress}/transactions/trc20?only_to=false&contract_address=${contractAddress}&min_timestamp=${time.valueOf()}&only_from=true`;
    const incomingUrl = `https://api.trongrid.io/v1/accounts/${walletAddress}/transactions/trc20?only_to=true&contract_address=${contractAddress}&min_timestamp=${time.valueOf()}`;

    Promise.all([
        fetchTransactions(outgoingUrl, 'out'),
        fetchTransactions(incomingUrl, 'in')
    ])
    .then(results => {
        const transactions = [].concat(...results);
        res.json(transactions);
    })
    .catch(error => {
        console.error(error);
        res.status(500).json({ error: 'An error occurred' });
    });
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
