const mongoose = require('mongoose');

mongoose.set("strictQuery", true);

mongoose.connect(process.env.DB_URI_1)
    .then(() => { console.log(`db connection successfully...`); })
    .catch((err) => { console.log(err); });