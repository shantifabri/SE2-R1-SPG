import { Button, Row } from 'react-bootstrap';

import API from '../API';
import ModalCreate from './ModalCreate';
import ModalManage from './ModalManage';
import ShowMeetings from './ShowMeetings';
//imports needed to use state
import React, { useState } from 'react';

function StudyGroup(props) {
    const nameClass = "justify-content-between group-badge color-button-" + props.color.toLowerCase();
    const removeGroup = () => {
        API.removeGroup(props.groupId)
        .then(props.setDirty(true));
    }

    return (<>
        <Row className={nameClass}>
            <span><b>{props.groupName}</b></span><span><b>{props.course}</b></span><span><Button variant="secondary" onClick={() => {props.setModalMeetings(true); props.setSelectedGroup(props.groupId)}}>Meetings</Button><Button variant="info" onClick={() => {props.setModal(true); props.setSelectedGroup(props.groupId)}}>Members</Button><Button variant="danger" onClick={() => removeGroup()}>X</Button></span>
        </Row>
    </>)
}

function AdminPanel(props) {
    const [modalMeetings, setModalMeetings] = useState(false);
    const [modalCreate, setModalCreate] = useState(false);
    const [modalManage, setModalManage] = useState(false);
    const [selectedGroup, setSelectedGroup] = useState(0);

    return (<>
        Administration!
        {props.availableGroups.map((group,index) => <StudyGroup key={group.groupId} setDirty={props.setDirty} setModalMeetings={setModalMeetings} setModal={setModalManage} setSelectedGroup={setSelectedGroup} groupName={group.groupName} course={group.course} groupId={group.groupId} credits={group.credits} color={group.color} joined={group.joined} requested={group.requested}/> )}
        {modalManage && <ModalManage setLoading={props.setLoading} selectedGroup={selectedGroup} setModal={setModalCreate} groupsMembers={props.groupsMembers} username={props.username} userId={props.userId} setDirty={props.setDirty}/> }
        {modalMeetings && <ShowMeetings setLoading={props.setLoading} selectedGroup={selectedGroup} setModal={setModalMeetings} allMeetings={props.allMeetings} setDirty={props.setDirty}/>}
        {modalCreate && <ModalCreate setLoading={props.setLoading} colorList={props.colorList} courseList={props.courseList} setModal={setModalCreate} username={props.username} userId={props.userId} setDirty={props.setDirty}/>}
        {props.loggedIn && <Button type="button" variant="primary" size="lg" className="fixed-left-bottom" onClick={() => {
            setModalCreate(true);
        }}>Add Group</Button>}
    </>)
}

export default AdminPanel;