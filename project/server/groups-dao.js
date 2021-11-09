'use strict';
/* Data Access Object (DAO) module for accessing memes */

const db = require('./db');


/**
 * Query the db to insert a new study group. Id will be automatically chosen by sqlite
 * @param {object} group group to insert into the db
 * @returns a promise
 */
exports.insertGroup = (group) => {
    return new Promise((resolve, reject) => {
        const sql = 'INSERT INTO studygroups (groupName, course, credits, color) VALUES(?, ?, ?, ?)';
        db.run(sql, [group.groupName, group.groupCourse, group.credits, group.color], function (err) {
            if (err){
                console.log(err);
                reject(err);
            } 
            else
                resolve();
        });
    });
};

/**
 * Query the db in order to accept a user join request. It performs a delete in order to remove the request
 * and then insert a new record in the useringroup table.
 * @param {number} groupId id of the group
 * @param {number} userId id of the user
 * @returns a promise
 */
 exports.acceptMember = (groupId, userId) => {
    return new Promise((resolve, reject) => {
        const sql = 'INSERT INTO useringroup (groupId, userId) VALUES(?, ?)';
        db.run(sql, [groupId, userId], function (err) {
            if (err){
                console.log(err);
                reject(err);
            } 
            else{
                const sql2 = 'DELETE FROM joinrequests where groupId = ? and userId = ?';
                db.run(sql2, [groupId, userId], function (err) {
                    if (err){
                        console.log(err);
                        reject(err);
                    } 
                });
                resolve();
            }
        });
    });
};

/**
 * Query the db to insert a new partecipation to a meeting
 * @param {number} userId id of the user
 * @param {number} meetingId id of the meeting
 * @returns a promise
 */
 exports.partecipateMeeting = (userId, meetingId) => {
    return new Promise((resolve, reject) => {
        const sql = 'INSERT INTO meetingpartecipants (userId, meetingId) VALUES(?, ?)';
        db.run(sql, [userId, meetingId], function (err) {
            if (err){
                console.log(err);
                reject(err);
            } 
            else
                resolve();
        });
    });
};

/**
 * Query the db to get all the colors used for the groups
 * @returns a promise that will resolve the list of colors already used
 */
exports.getColors = () => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT distinct color from studygroups";
        db.all(sql, [], (err, rows) => {
            if (err)
                reject(err);
            else
                resolve(rows);
        });
    });
}

/**
 * Query the db to get all the courses already used
 * @returns a promise that will resolve to the list of courses that already have a study group
 */
exports.getCourses = () => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT distinct course from studygroups";
        db.all(sql, [], (err, rows) => {
            if (err)
                reject(err);
            else
                resolve(rows);
        });
    });
}

/**
 * Query the db to get all the available study groups
 * @param {number} userId id of the user
 * @returns a promise that will resolve to the list of all study groups retrieved from the db
 */
exports.getAvailableGroups = (userId) => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT distinct a.*, CASE WHEN b.groupId is NULL THEN 0 ELSE 1 END as requested FROM (SELECT distinct s.groupId, groupName, course, credits, color,CASE WHEN u.role is NULL then 0 else u.role END as role, CASE WHEN u.groupId is null THEN 0 ELSE 1 end as joined from studygroups s left join (select distinct userId,groupId,role from useringroup where userId = ?) u on s.groupId = u.groupId)a left join (select distinct userId,groupId from joinrequests where userId = ?)b on b.groupId = a.groupId";
        db.all(sql, [userId,userId], (err, rows) => {
            if (err){
                console.log(err);
                reject(err);
            }
            else
                resolve(rows);
        });
    });
}

/**
 * Query the db to get all the meetings of a certain user
 * @returns a promise that will resolve to the list of meetings of a certain user
 */
 exports.getPersonalMeetings = (userId) => {
    return new Promise((resolve, reject) => {
        const sql = "select distinct c.*,CASE WHEN m.partecipationId IS NULL THEN 0 ELSE 1 END as partecipates from (select a.*,color from (select title,description,dateStart,dateEnd,meetingId,m.groupId,userId from meetings m join useringroup u on u.groupId = m.groupId where userId = ?) a join studygroups s on a.groupId=s.groupId order by dateStart)c left join meetingpartecipants m on m.meetingId = c.meetingId and m.userId = c.userId ";
        db.all(sql, [userId], (err, rows) => {
            if (err){
                console.log(err);
                reject(err);
            }
            else
                resolve(rows);
        });
    });
}

/**
 * Query the db to get all the meetings for all the groups
 * @returns a promise that will resolve to the list of all meetings retrieved from the db
 */
 exports.getAllMeetings = () => {
    return new Promise((resolve, reject) => {
        const sql = "select distinct m.*,color from meetings m join studygroups s on m.groupId = s.groupId order by dateStart";
        db.all(sql, [], (err, rows) => {
            if (err){
                console.log(err);
                reject(err);
            }
            else{
                const meetings = rows.map((e) => ({
                    meetingId: e.meetingId,
                    dateStart: e.dateStart,
                    title: e.title,
                    groupId: e.groupId,
                    location: e.location,
                    duration: e.duration,
                    color: e.color
                }));
    
                const meetingsGroup = {};
                meetings.map((meeting) => {
                    if(meetingsGroup[meeting.groupId]){
                        meetingsGroup[meeting.groupId].push(meeting);
                    }
                    else {
                        meetingsGroup[meeting.groupId] = [];
                        meetingsGroup[meeting.groupId].push(meeting);
                    }
                });
                resolve(meetingsGroup);
            }
                
        });
    });
}

/**
 * Query the db to get all the join requests to the various groups
 * @returns a promise that will resolve to the list of join requests retrieved from the db
 */
 exports.getJoiners = () => {
    return new Promise((resolve, reject) => {
        const sql = "select distinct j.*, name, email from joinrequests j join users u on j.userId = u.id";
        db.all(sql, [], (err, rows) => {
            if (err){
                console.log(err);
                reject(err);
            }
            else{
                const joiners = rows.map((e) => ({
                    userId: e.userId,
                    groupId: e.groupId,
                    name: e.name,
                    email: e.email
                }));
    
                const groupJoiners = {};
                joiners.map((joiner) => {
                    if(groupJoiners[joiner.groupId]){
                        groupJoiners[joiner.groupId].push(joiner);
                    }
                    else {
                        groupJoiners[joiner.groupId] = [];
                        groupJoiners[joiner.groupId].push(joiner);
                    }
                });
                resolve(groupJoiners);
            }
                
        });
    });
}

/**
 * Query the db to get all the members of each study group
 * @returns a promise that will resolve to the list of all members of each study group retrieved from the db
 */
exports.getGroupsMembers = () => {
    return new Promise((resolve, reject) => {
        const sql = 'SELECT distinct groupId,userId,role,name,email from useringroup join users on userId=id';
        db.all(sql, [], (err, rows) => {
            if (err) {
                reject(err);
                console.log(err);
                return;
            }

            const members = rows.map((e) => ({
                groupId: e.groupId,
                userId: e.userId,
                role: e.role,
                name: e.name,
                email: e.email
            }));

            const groups = {};
            members.map((member) => {
                if(groups[member.groupId]){
                    groups[member.groupId].push(member);
                }
                else {
                    groups[member.groupId] = [];
                    groups[member.groupId].push(member);
                }
            });

            resolve(groups);
        });
    });
};

/**
 * Query the db to insert a new join request. Id will be automatically chosen by sqlite
 * @param {number} groupId id of the group to insert in the db
 * @param {number} userId id of the user who's doing the request
 * @returns a promise that will resolve
 */
 exports.insertRequest = (groupId, userId) => {
    return new Promise((resolve, reject) => {
        const sql = 'INSERT INTO joinrequests (userId, groupId) VALUES(?, ?)';
        db.run(sql, [userId,groupId], function (err) {
            if (err){
                console.log(err);
                reject(err);
            } 
            else
                resolve();
        });
    });
};

/**
 * Query the db to change the role of a certain user in a certain group
 * @param {number} userId id of the user
 * @param {number} groupId id of the group
 * @param {number} role new role to be assigned to the user
 * @returns a promise that will resolve
 */
 exports.changeRole = (userId, groupId, role) => {
    return new Promise((resolve, reject) => {
        const sql = 'UPDATE useringroup set role = ? where userId = ? and groupId = ?';
        db.run(sql, [role,userId,groupId], function (err) {
            if (err){
                console.log(err);
                reject(err);
            } 
            else
                resolve();
        });
    });
};

/**
 * Query the db to create a new meeting for a specified group.
 * @param {string} title title of the meeting
 * @param {string} description description of the meeting
 * @param {string} dateStart start date of the meeting
 * @param {string} dateEnd end date of the meeting
 * @param {number} groupId id of the group
 * @param {number} duration duration of the meeting in minutes
 * @param {string} location location place of the meeting
 * @returns a promise that will resolve
 */
 exports.createMeeting = (title, description, dateStart, dateEnd, groupId, duration, location) => {
    return new Promise((resolve, reject) => {
        const sql = 'INSERT INTO meetings (title, description, dateStart, dateEnd, groupId, duration, location) VALUES(?, ?, ?, ?, ?, ?, ?)';
        db.run(sql, [title,description,dateStart,dateEnd,groupId,duration,location], function (err) {
            if (err){
                console.log(err);
                reject(err);
            } 
            else
                resolve();
        });
    });
};

/**
 * Query the db to remove a user from a certain group and removes also the partecipation of that user in all the meetings of the specified group
 * @param {number} userId id of the user
 * @param {number} groupId id of the group
 * @returns a promise that will resolve
 */
 exports.removeUserFromGroup = (userId, groupId) => {
    return new Promise((resolve, reject) => {
        const sql = 'DELETE FROM useringroup WHERE userId = ? AND groupId = ?';
        db.run(sql, [userId, groupId], function (err) {
            if (err)
                reject(err);
            else if (this.changes === 0)
                reject({
                    errors: [{
                        value: userId, msg: "The userId is wrong and does not exist in the selected group!",
                        param: "id", location: "params"
                    }]
                })
            else{
                const sql2 = 'DELETE FROM meetingpartecipants WHERE userId = ? AND meetingId IN (select distinct meetingId from meetings where groupId = ?)';
                db.run(sql2, [userId, groupId], function (err) {
                    if (err)
                        reject(err);
                    else {
                        resolve();
                    }
                });
            }
        });
    });
}

/**
 * Query the db to delete the partecipation of a certain user from a certain group
 * @param {number} userId id of the user
 * @param {number} meetingId id of the meeting
 * @returns a promise that will resolve
 */
 exports.unpartecipateMeeting = (userId, meetingId) => {
    return new Promise((resolve, reject) => {
        const sql = 'DELETE FROM meetingpartecipants WHERE userId = ? AND meetingId = ?';
        db.run(sql, [userId, meetingId], function (err) {
            if (err)
                reject(err);
            else if (this.changes === 0)
                reject({
                    errors: [{
                        value: userId, msg: "The userId is wrong and is not partecipating to the selected meeting!",
                        param: "id", location: "params"
                    }]
                })
            else{
                resolve();
            }
        });
    });
}

/**
 * Query the db to remove a certain group from the db
 * @param {number} groupId id of the group to delete
 * @returns a promise that will resolve
 */
 exports.removeGroup = (groupId) => {
    return new Promise((resolve, reject) => {
        const sql = 'DELETE FROM studygroups WHERE groupId = ?';
        db.run(sql, [groupId], function (err) {
            if (err)
                reject(err);
            else if (this.changes === 0)
                reject({
                    errors: [{
                        value: userId, msg: "A Study Group with the selected id does not exist!",
                        param: "id", location: "params"
                    }]
                })
            else{
                resolve();
            }
        });
    });
}