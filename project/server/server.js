'use strict';

//Require express
const express = require('express');
//Require a logging middleware that is useful for debugging purposes: morgan
const morgan = require('morgan');
//Require passport
const passport = require('passport');
//Require LocalStrategy for authentication with username and password
const LocalStrategy = require('passport-local').Strategy;
//Require session
const session = require('express-session');
//Require express-validator which is used to perform validation
const { body, validationResult, param } = require('express-validator');

// init express
const app = new express();
const PORT = 3001;
app.use(morgan('dev'));
app.use(express.json());

//Require the dao module for accessing users in DB
const userDao = require('./user-dao');

const groupsDao = require('./groups-dao');

/*** Set up Passport ***/
// set up the "username and password" login strategy
// by setting a functcdion to verify username and password
passport.use(new LocalStrategy(
    function (username, password, done) {
        userDao.getUser(username, password).then((user) => {
            if (!user)
                return done(null, false, { message: 'Incorrect username and/or password.' });

            return done(null, user);
        })
    }
));

// serialize and de-serialize the user (user object <-> session)
// we serialize the user id and we store it in the session: the session is very small in this way
passport.serializeUser((user, done) => {
    done(null, user.id);
});

// starting from the data in the session, we extract the current (logged-in) user
passport.deserializeUser((id, done) => {
    userDao.getUserById(id)
        .then(user => {
            done(null, user); // this will be available in req.user
        }).catch(err => {
            done(err, null);
        });
});

// activate the server
app.listen(PORT, () => {
    console.log(`Server listening at http://localhost:${PORT}`);
});

// custom middleware: check if a given request is coming from an authenticated user
const isLoggedIn = (req, res, next) => {
    if (req.isAuthenticated())
        return next();

    return res.status(401).json({ error: 'not authenticated' });
}

// set up the session
app.use(session({
    // by default, Passport uses a MemoryStore to keep track of the sessions
    //a secret sentence not to share with anybody and anywhere, used to sign the session ID cookie
    secret: '0Ws0TQxSueD0eFNepQgrsE1j5RMU68xB89wOkgANHGAS4RwomWhYiX031QmrOqqT5B8GJ8nPmVHusvDuxVyWp1zZmTL$EdWqP2e4htDjDZabw0YOrAaam6w0pt7LkZcL',
    resave: false,
    saveUninitialized: false,
    cookie: {
        sameSite: 'strict'
    }
}));

// then, init passport
app.use(passport.initialize());
app.use(passport.session());

/*** STATIC CONTENT ***/
//Serving static requests
app.use('/static', express.static('public'))

/*** Users APIs ***/

// POST /api/sessions 
// login
app.post('/api/sessions', function (req, res, next) {
    passport.authenticate('local', (err, user, info) => {
        if (err)
            return next(err);
        if (!user) {
            // display wrong login messages
            return res.status(401).json(info);
        }
        // success, perform the login
        req.login(user, (err) => {
            if (err)
                return next(err);

            // req.user contains the authenticated user, we send all the user info back
            // this is coming from userDao.getUser()
            return res.json(req.user);
        });
    })(req, res, next);
});

// DELETE /api/sessions/current 
// logout
app.delete('/api/sessions/current', (req, res) => {
    req.logout();
    res.end();
});

// GET /api/sessions/current
// check whether the user is logged in or not
app.get('/api/sessions/current', (req, res) => {
    if (req.isAuthenticated()) {
        res.status(200).json(req.user);
    }
    else
        res.status(401).json({ error: 'Unauthenticated user!' });
});

////////////////////////////////////////////////////////////////////////////////////////

//POST: Save a new group into the db.
app.post('/api/newGroup', isLoggedIn, async (req, res) => {
    //Perform validation. withMessage is used to print custom error messages. bail is used to block the chain of validation when it has already failed.
    await Promise.all([
        //GroupName must be a string of at least 3 chars
        body('groupName').isString().withMessage("Must be a string").bail().isLength({ min: 3 }).withMessage("Must be at least 3 chars long").run(req),
        //GroupCourse must be a string of at least 3 chars
        body('groupCourse').isString().withMessage("Must be a string").bail().isLength({ min: 3 }).withMessage("Must be at least 3 chars long").run(req),
        body('color').isString().withMessage("Must be a string").run(req),
        body('credits').isInt().withMessage("Must be an Integer").run(req)
    ]);
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        //If there are errors then return status 422 and the object with the array of errors
        return res.status(422).json({ errors: errors.array() });
    }
    groupsDao.insertGroup(req.body, req.user.id)
        .then(groupId => res.status(201))
        .catch(err => res.status(500).json(err));
});

//GET: Retrieve all the colors used for the various groups.
app.get('/api/getColors', (req, res) => {
    groupsDao.getColors()
        .then(colors => res.status(200).json(colors))
        .catch(err => res.status(500).json(err));
});

//GET: Retrieve all the courses used for the various groups.
app.get('/api/getCourses', (req, res) => {
    groupsDao.getCourses()
        .then(colors => res.status(200).json(colors))
        .catch(err => res.status(500).json(err));
});

//GET: Retrieve all the studygroups the user is not registered to.
app.get('/api/getAvailableGroups/:userId', (req, res) => {
    groupsDao.getAvailableGroups(req.params.userId)
        .then(groups => res.status(200).json(groups))
        .catch(err => res.status(500).json(err));
});

//GET: Retrieve all the studygroups the user is not registered to.
app.get('/api/getPersonalMeetings/:userId', (req, res) => {
    groupsDao.getPersonalMeetings(req.params.userId)
        .then(meetings => res.status(200).json(meetings))
        .catch(err => res.status(500).json(err));
});

//GET: Retrieve all the studygroups the user is not registered to.
app.get('/api/getAllMeetings', (req, res) => {
    groupsDao.getAllMeetings()
        .then(meetings => res.status(200).json(meetings))
        .catch(err => res.status(500).json(err));
});

//GET: Retrieve all the studygroups the user is not registered to.
app.get('/api/getGroupsMembers', (req, res) => {
    groupsDao.getGroupsMembers()
        .then(groups => res.status(200).json(groups))
        .catch(err => res.status(500).json(err));
});

//GET: Retrieve all the studygroups the user is not registered to.
app.get('/api/getJoiners', (req, res) => {
    groupsDao.getJoiners()
        .then(groups => res.status(200).json(groups))
        .catch(err => res.status(500).json(err));
});

app.post('/api/insertRequest', isLoggedIn, async (req, res) => {
    //Perform validation. withMessage is used to print custom error messages. bail is used to block the chain of validation when it has already failed.
    await Promise.all([
        body('groupId').isInt().withMessage("Group Id must be an Integer").run(req),
        body('userId').isInt().withMessage("User Id must be an Integer").run(req)
    ]);
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        //If there are errors then return status 422 and the object with the array of errors
        console.log(errors)
        return res.status(422).json({ errors: errors.array() });
    }
    groupsDao.insertRequest(req.body.groupId, req.body.userId)
        .then(groupId => res.status(201))
        .catch(err => res.status(500).json(err));
});

app.post('/api/changeRole', isLoggedIn, async (req, res) => {
    //Perform validation. withMessage is used to print custom error messages. bail is used to block the chain of validation when it has already failed.
    await Promise.all([
        body('groupId').isInt().withMessage("Group Id must be an Integer").run(req),
        body('userId').isInt().withMessage("User Id must be an Integer").run(req),
        body('role').isInt().withMessage("Role must be an Integer").run(req)
    ]);
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        //If there are errors then return status 422 and the object with the array of errors
        console.log(errors)
        return res.status(422).json({ errors: errors.array() });
    }
    groupsDao.changeRole(req.body.userId, req.body.groupId, req.body.role)
        .then(() => res.status(201))
        .catch(err => res.status(500).json(err));
});

app.post('/api/acceptMember', isLoggedIn, async (req, res) => {
    //Perform validation. withMessage is used to print custom error messages. bail is used to block the chain of validation when it has already failed.
    await Promise.all([
        body('groupId').isInt().withMessage("Group Id must be an Integer").run(req),
        body('userId').isInt().withMessage("User Id must be an Integer").run(req)
    ]);
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        //If there are errors then return status 422 and the object with the array of errors
        console.log(errors)
        return res.status(422).json({ errors: errors.array() });
    }
    groupsDao.acceptMember(req.body.groupId, req.body.userId)
        .then(groupId => res.status(201))
        .catch(err => res.status(500).json(err));
});

app.post('/api/partecipateMeeting', isLoggedIn, async (req, res) => {
    //Perform validation. withMessage is used to print custom error messages. bail is used to block the chain of validation when it has already failed.
    await Promise.all([
        body('userId').isInt().withMessage("User Id must be an Integer").run(req),
        body('meetingId').isInt().withMessage("Meeting Id must be an Integer").run(req)
    ]);
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        //If there are errors then return status 422 and the object with the array of errors
        console.log(errors)
        return res.status(422).json({ errors: errors.array() });
    }
    groupsDao.partecipateMeeting(req.body.userId, req.body.meetingId)
        .then(userId => res.status(201))
        .catch(err => res.status(500).json(err));
});

app.post('/api/createMeeting', isLoggedIn, async (req, res) => {
    //Perform validation. withMessage is used to print custom error messages. bail is used to block the chain of validation when it has already failed.
    await Promise.all([
        body('title').isString().withMessage("Title must be a String").run(req),
        body('description').isString().withMessage("Description must be a String").run(req),
        body('location').isString().withMessage("Location must be a String").run(req),
        body('duration').isInt().withMessage("Duration must be an Integer").run(req)
        // body('date').isString().withMessage("Date must be a String").run(req)
    ]);
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        //If there are errors then return status 422 and the object with the array of errors
        console.log(errors)
        return res.status(422).json({ errors: errors.array() });
    }
    groupsDao.createMeeting(req.body.title, req.body.description, req.body.dateStart, req.body.dateEnd, req.body.groupId, req.body.duration, req.body.location)
        .then(meetingId => res.status(201))
        .catch(err => res.status(500).json(err));
});

//DELETE: Delete an existing user from a group
app.delete('/api/removeUserFromGroup', isLoggedIn, async (req, res) => {
    await Promise.all([
        body('groupId').isInt().withMessage("Group Id must be an Integer").run(req),
        body('userId').isInt().withMessage("User Id must be an Integer").run(req)
    ]);
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        //If there are errors then return status 422 and the object with the array of errors
        console.log(errors)
        return res.status(422).json({ errors: errors.array() });
    }

    groupsDao.removeUserFromGroup(req.body.userId, req.body.groupId)
        .then(() => res.status(200).json({ "id of the deleted user": req.body.userId, "outcome": "success" }))
        .catch(err => {
            if (err.errors){
                console.log(err);
                res.status(404).json(err);
            }
            else
                res.status(500).json(err);
        });
});

//DELETE: Delete an existing group
app.delete('/api/removeGroup', isLoggedIn, async (req, res) => {
    await Promise.all([
        body('groupId').isInt().withMessage("Group Id must be an Integer").run(req)
    ]);
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        //If there are errors then return status 422 and the object with the array of errors
        console.log(errors)
        return res.status(422).json({ errors: errors.array() });
    }

    groupsDao.removeGroup(req.body.groupId)
        .then(() => res.status(200).json({ "id of the deleted user": req.body.groupId, "outcome": "success" }))
        .catch(err => {
            if (err.errors){
                console.log(err);
                res.status(404).json(err);
            }
            else
                res.status(500).json(err);
        });
});

//DELETE: Remove a partecipant from a meeting.
app.delete('/api/unpartecipateMeeting', isLoggedIn, async (req, res) => {
    await Promise.all([
        body('meetingId').isInt().withMessage("Meeting Id must be an Integer").run(req),
        body('userId').isInt().withMessage("User Id must be an Integer").run(req)
    ]);
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        //If there are errors then return status 422 and the object with the array of errors
        console.log(errors)
        return res.status(422).json({ errors: errors.array() });
    }

    groupsDao.unpartecipateMeeting(req.body.userId, req.body.meetingId)
        .then(() => res.status(200).json({ "id of the deleted user": req.body.userId, "outcome": "success" }))
        .catch(err => {
            if (err.errors){
                console.log(err);
                res.status(404).json(err);
            }
            else
                res.status(500).json(err);
        });
});
