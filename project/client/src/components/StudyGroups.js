import { Button, Row } from 'react-bootstrap';
//import images
//import my CSS
import '../mycss/custom.css';
import API from '../API';
//imports needed to use state
import React from 'react';

function StudyGroup(props) {
    const handleSubmit = (event) => {
        props.setDirty(true);
        API.insertRequest(props.groupId,props.userId)
        .then(() => {
            props.setDirty(true);
        });

    }

    const nameClass = "justify-content-between group-badge color-button-" + props.color.toLowerCase();
    const disab = props.requested || props.joined;
    return (<>
        <Row className={nameClass}>
            <span><b>{props.groupName}</b></span><span><b>{props.course}</b></span><Button disabled={disab} onClick={handleSubmit}>Request Join</Button>
        </Row>
    </>)
}

function StudyGroups(props) {
    return (<>
        StudyGroups!
        {props.availableGroups.map((group,index) => <StudyGroup key={group.groupId} userId={props.userId} setDirty={props.setDirty} groupId={group.groupId} groupName={group.groupName} course={group.course} credits={group.credits} color={group.color} joined={group.joined} requested={group.requested}/> )}
    </>)
}

export default StudyGroups;