//import react-bootstrap components
import { Button, Modal, Container, Row, Col, Form } from 'react-bootstrap';
//imports needed to use state
import React, { useState } from 'react';
import API from '../API';


// modal opened in the manage group section, it shows all the members of a study group and all the join requests.
// this modal allows to accept join requests and remove group members which are not group admins.
function Joiner(props){
    const myClass = "justify-content-between pending-requests";

    const acceptMember = () => {
        API.acceptMember(props.groupId,props.userId)
        .then(() => {
            props.setDirty(true);
        })
    }

    return(
        <Row className={myClass}><span className="accept-button">{props.name}</span><span className="accept-button">{props.email}</span><span><Button className="accept-button" onClick={() => {acceptMember();props.setDirty(true);props.setLoading(true)}}>Accept</Button></span></Row>
    )
}

function Members(props) {
    const handleRemove = (userId,groupId) => {
        API.removeUserFromGroup(userId,groupId)
        .then(() => props.setDirty(true));
        
    }

    return (<>
        <Form>
            <p className="italic-text">
                Remove Members and Accept/Decline Join Requests {props.groupName}
            </p>
            <Form.Row>
                {props.groupJoiners &&  
                    <Form.Group as={Col} xs="12" controlId="titleForm" >
                        <b>Pending</b>
                        {props.groupJoiners.map((joiner) => 
                            <Joiner key={joiner.userId} email={joiner.email} name={joiner.name} userId={joiner.userId} groupId={joiner.groupId} setDirty={props.setDirty} setLoading={props.setLoading}/>
                        )}
                    </Form.Group>
                }
                {props.groupsMembers &&
                    <Form.Group as={Col} xs="12" controlId="titleForm">
                        <b>Members</b>
                        {props.groupsMembers.map((member) => 
                            <Row key={member.id} className="justify-content-between"><span>{member.name}</span><span>{member.role === 1 ? "group admin" : "member"}</span><span><Button variant="danger" disabled={member.role === 1} onClick={() => handleRemove(member.userId,props.selectedGroup)}>X</Button></span></Row>  
                        )}
                    </Form.Group>
                }
            </Form.Row>
        </Form>
    </>)
}

function ModalMembers(props) {
    const modalTitle = "Manage Group Members";

    const [groupName, setGroupName] = useState("");
    const [groupCourse, setGroupCourse] = useState("");

    return (
        <Modal show={true} onHide={() => {
            props.setModal(false);
            props.setLoading(true);
            props.setDirty(true);
        }} backdrop="static" keyboard={false} centered animation={false} size={"lg"}>
            <Modal.Header closeButton>
                <Modal.Title>{modalTitle}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Container>
                    <Members selectedGroup={props.selectedGroup} groupJoiners={props.groupJoiners[props.selectedGroup]} groupsMembers={props.groupsMembers[props.selectedGroup]} courseList={props.courseList} setName={setGroupName} name={groupName} setCourse={setGroupCourse} course={groupCourse} setDirty={props.setDirty} setLoading={props.setLoading}/>
                </Container>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={() => {
                    props.setModal(false);
                    props.setLoading(true);
                    props.setDirty(true);
                }}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    )
}

export default ModalMembers;