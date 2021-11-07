import { Button, Row } from 'react-bootstrap';
//import images

//imports needed to use state
import React, { useState } from 'react';

import ModalMeetings from './ModalMeetings';
import ModalMembers from './ModalMembers';

function Group(props) {
    const nameClass = "justify-content-between group-badge color-button-" + props.color.toLowerCase();
    return (<>
        <Row className={nameClass}>
            <span><b>{props.groupName}</b></span><span><b>{props.course}</b></span><span><Button variant="secondary" onClick={() => {props.setModalMeetings(true);props.setSelectedGroup(props.groupId)}}>Meetings</Button><Button variant="info" onClick={() => {props.setModalMembers(true);props.setSelectedGroup(props.groupId)}}>Members</Button></span>
        </Row>
    </>)
}

function ManageGroups(props) {
    const [modalMeetings,setModalMeetings] = useState(false);
    const [modalMembers, setModalMembers] = useState(false);
    const [selectedGroup, setSelectedGroup] = useState(0);
    // page that allows to manage the groups that the user can manage (is admin of).
    // the managing works through 2 modals, one for the members and one for the meetings
    return (<>
        Manage the Groups!
        {modalMembers && <ModalMembers setModal={setModalMembers} groupJoiners={props.groupJoiners} selectedGroup={selectedGroup} groupsMembers={props.groupsMembers} setLoading={props.setLoading} setDirty={props.setDirty}/>}
        {modalMeetings && <ModalMeetings setModal={setModalMeetings} allMeetings={props.allMeetings} selectedGroup={selectedGroup} setLoading={props.setLoading} setDirty={props.setDirty}/>}
        {props.availableGroups.map((group) => group.role === 1 && <Group key={group.groupId} setSelectedGroup={setSelectedGroup} setModalMembers={setModalMembers} setModalMeetings={setModalMeetings} groupId={group.groupId} groupName={group.groupName} course={group.course} credits={group.credits} color={group.color} joined={group.joined} requested={group.requested}/> )}
    </>)
}

export default ManageGroups;