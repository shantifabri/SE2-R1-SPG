'use strict';
/* Data Access Object (DAO) module for accessing users (which in this case are creators)*/

const db = require('./db');
const bcrypt = require('bcrypt');

/**
 * Query the db to get the info of a user given its id
 * @param {Number} id of the user whose info should be retrieved
 * @returns a promise that will resolve to an object containing user info
 */
exports.getUserById = (id) => {
    return new Promise((resolve, reject) => {
        const sql = 'SELECT * FROM users WHERE id = ?';
        db.get(sql, [id], (err, row) => {
            if (err)
                reject(err);
            else if (row === undefined)
                resolve({ error: 'User not found.' });
            else {
                // by default, the local strategy looks for "username": not to create confusion in server.js, we can create an object with that property
                const user = { id: row.id, username: row.email, name: row.name, admin: row.admin }
                resolve(user);
            }
        });
    });
};

/**
 * Query the db to get the info of a user given its email, only if password is correct
 * @param {string} email email of the user whose info should be retrieved
 * @param {string} password password of the user, which should match with the one (hashed) in the database
 * @returns a promise that will resolve to an object containing user info
 */
exports.getUser = (email, password) => {
    return new Promise((resolve, reject) => {
        const sql = 'SELECT * FROM users WHERE email = ?';
        db.get(sql, [email], (err, row) => {
            if (err)
                reject(err);
            else if (row === undefined) {
                resolve(false);
            }
            else {
                const user = { id: row.id, username: row.email, name: row.name, admin: row.admin };

                bcrypt.compare(password, row.hash).then(result => {
                    if (result)
                        resolve(user);
                    else
                        resolve(false);
                });
            }
        });
    });
};