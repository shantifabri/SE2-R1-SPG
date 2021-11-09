import dayjs from "dayjs";

const url = 'http://localhost:3000';
 
// STUDY GROUP APIs //////////////////////////////////////////////////////////////////7

/* Allows create a new Study Group giving some information */
async function addNewGroup(newGroup) {
    await fetch(url + '/api/newGroup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            groupName: newGroup.groupName,
            groupCourse: newGroup.groupCourse,
            color: newGroup.color,
            credits: newGroup.credits
        })
    });
}

/* Allows to get the list of colors already used for the study groups */
async function getColors() {
    const response = await fetch(url + '/api/getColors');
    if (response.ok) {
        return response.json();
    }
    return [];
}

/* Allows to retrieve the list of courses for which a study group already exists */
async function getCourses() {
    const response = await fetch(url + '/api/getCourses');
    if (response.ok) {
        return response.json();
    }
    return [];
}

/* Allows to retrieve all the groups of a certain user */
async function getAvailableGroups(userId) {
    const response = await fetch(url + '/api/getAvailableGroups/' + userId);
    if (response.ok) {
        return response.json();
    }
    return [];
}

/* Allows to retrieve all the meetings of a certain user according to the study groups joined */
async function getPersonalMeetings(userId) {
    const response = await fetch(url + '/api/getPersonalMeetings/' + userId);
    if (response.ok) {
        return response.json();
    }
    return [];
}

/* Allows to retrieve all the meetings of all the studygroups */
async function getAllMeetings() {
    const response = await fetch(url + '/api/getAllMeetings');
    if (response.ok) {
        return response.json();
    }
    return [];
}

/* Allows to retrieve all the members of each study group */
async function getGroupsMembers() {
    const response = await fetch(url + '/api/getGroupsMembers');
    if (response.ok) {
        return response.json();
    }
    return [];
}

/* Allows to retrieve the list of users with a pending join request for each group */
async function getJoiners() {
    const response = await fetch(url + '/api/getJoiners');
    if (response.ok) {
        return response.json();
    }
    return [];
}

/* Allows to insert a new join request for a certain user in a certain group */
async function insertRequest(groupId,userId) {
    await fetch(url + '/api/insertRequest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            groupId: groupId,
            userId: userId
        })
    });
}

/* Allows to change the role of a certain user in a certain group */
async function changeRole(userId,groupId,role) {
    await fetch(url + '/api/changeRole', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            userId: userId,
            groupId: groupId,
            role: role
        })
    });
}

/* Allows to accept a join request for a certain user in a certain group */
async function acceptMember(groupId,userId) {
    await fetch(url + '/api/acceptMember', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            groupId: groupId,
            userId: userId
        })
    });
}

/* Allows a user to partecipate a certain meeting given a meeting Id */
async function partecipateMeeting(userId,meetingId) {
    await fetch(url + '/api/partecipateMeeting', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            userId: userId,
            meetingId: meetingId
        })
    });
}

/* Allows a user to unpartecipate a meeting deleting a meeting partecipation from the DB */
async function unpartecipateMeeting(userId,meetingId) {
    await fetch(url + '/api/unpartecipateMeeting', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            userId: userId,
            meetingId: meetingId
        })
    });
}

/* Allows a user to create a new meeting for a certain group */
async function createMeeting(title,description,date,groupId,duration,location) {
    await fetch(url + '/api/createMeeting', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: title,
            description: description,
            dateStart: date,
            dateEnd: dayjs(date).add(duration, 'minute'),
            groupId: groupId,
            duration: duration,
            location: location
        })
    });
}

/**
 * Function that performs a DELETE request to the server to delete an existing user in group with given userId and groupId.
 * @param {number} userId id of the user
 * @param {number} groupId id of the groups
 */
 async function removeUserFromGroup(userId,groupId) {
    await fetch(url + '/api/removeUserFromGroup', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            groupId: groupId,
            userId: userId
        })
    });
}

/**
 * Function that performs a DELETE request to the server to delete an existing group with given id.
 * @param {number} groupId Id of the group to delete on the server
 */
 async function removeGroup(groupId) {
    await fetch(url + '/api/removeGroup', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            groupId: groupId
        })
    });
}

////////////////////////////////////////////////////////////////////////////////////


/**
 * Function that performs the login through a POST request to the server
 * @param {object} credentials object with username and password of the user that wants to log in 
 * @returns an object with the user name and the user id
 */
async function logIn(credentials) {
    let response = await fetch(url + '/api/sessions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
    });
    if (response.ok) {
        const user = await response.json();
        return { name: user.name, id: user.id, admin: user.admin };
    }
    else {
        try {
            const errDetail = await response.json();
            throw errDetail.message;
        }
        catch (err) {
            throw err;
        }
    }
}

/**
 * Function that performs the logout through a DELETE request to the server
 */
async function logOut() {
    await fetch(url + '/api/sessions/current', { method: 'DELETE' });
}

/**
 * Function that checks wheather a user is logged in or not through a GET request to the server
 * @returns an object with the user info (id, username, name)
 */
async function getUserInfo() {
    const response = await fetch(url + '/api/sessions/current');
    const userInfo = await response.json();
    if (response.ok) {
        return userInfo;
    } else {
        throw userInfo;  // an object with the error coming from the server
    }
}



const API = { logIn, logOut, getUserInfo, addNewGroup, getColors, getCourses, getAvailableGroups, insertRequest, getGroupsMembers, removeUserFromGroup, createMeeting, getPersonalMeetings, getAllMeetings, partecipateMeeting, getJoiners, acceptMember, unpartecipateMeeting, changeRole, removeGroup }

export default API;