//import react-bootstrap components
import { Button, Modal, Container, Row, Col, Form } from 'react-bootstrap';
//imports needed to use state
import React, { useState } from 'react';
import API from '../API';


// modals opened from the admin panel which allows to see all the members of a study group and change their role.
// change from admin to member.
function Member(props) {
    const changeRole = () => {
        let newRole = 1;
        if(props.role === 1)
            newRole = 0;

        API.changeRole(props.userId,props.groupId,newRole)
        .then();        
    }

    return(
        <>
            <Row className="justify-content-between"><span>{props.name}</span><span>{props.email}</span><span>{props.role === 1 ? <Button variant="info" onClick={() => {changeRole();props.setDirty(true);}}>Group Admin</Button> : <Button variant="info" onClick={() => {changeRole();props.setDirty(true)}}>Member</Button>}</span></Row>
        </>
    )
}

function GroupForm(props) {
    return (<>
        <Form>
            <p className="italic-text">
                Manage Members of the Group: {props.groupName}
            </p>
            <Form.Row>
                {props.groupsMembers ? 
                    <Form.Group as={Col} xs="12" controlId="titleForm">
                        {props.groupsMembers.map((member) => 
                            <Member key={member.userId} groupId={props.selectedGroup} name={member.name} email={member.email} userId={member.userId} role={member.role} setDirty={props.setDirty}/>  
                        )}
                    </Form.Group>
                : <></>}
            </Form.Row>
        </Form>
    </>)
}

function ModalManage(props) {
    const modalTitle = "Manage Group Members";
    const [title, setTitle] = useState("");

    const [groupName, setGroupName] = useState("");
    const [groupCourse, setGroupCourse] = useState("");

    const [color, setColor] = useState("");
    const [credits, setCredits] = useState(undefined);

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
                    <GroupForm colorList={props.colorList} selectedGroup={props.selectedGroup} groupsMembers={props.groupsMembers[props.selectedGroup]} courseList={props.courseList} setTitle={setTitle} title={title} setName={setGroupName} name={groupName} setCourse={setGroupCourse} course={groupCourse} setColor={setColor} color={color} setCredits={setCredits} credits={credits} setDirty={props.setDirty}></GroupForm>
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

export default ModalManage;