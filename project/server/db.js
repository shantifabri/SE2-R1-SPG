'use strict';
//Require sqlite3
const sqlite = require('sqlite3');

//Open the database
const db = new sqlite.Database('studygroups.db', (err) => {
    if (err)
        throw (err);
    else
        console.log("DB successfully opened");
});

module.exports = db;