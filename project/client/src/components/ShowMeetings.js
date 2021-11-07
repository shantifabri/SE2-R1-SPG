//import react-bootstrap components
import { Button, Modal, Container, Row, Col, Form } from 'react-bootstrap';
//imports needed to use state
import React from 'react';
import dayjs from 'dayjs';
import UTILS from '../Utils';

// modal that opens on the administration page to show all the past and future meetings of a certain study group.
function Meeting(props) {
    const newClass = UTILS.groupColor[props.color] + " group-badge justify-content-between";
    return(
        <>
            <Row className={newClass}><span><b>{props.title}</b></span><span><b>{dayjs(props.dateStart).format('ddd D MMM YYYY [at] H:m')}</b></span></Row>
        </>
    )
}

function Meetings(props) {
    return (<>
        <Form>
            <p className="italic-text">
                Check the Meetings of the Group:
            </p>
            <Form.Row>
                {props.meetings ? 
                    <Form.Group as={Col} xs="12" controlId="titleForm">
                        {props.meetings.map((meeting) => 
                            <Meeting key={meeting.meetingId} color={meeting.color} groupId={meeting.groupId} title={meeting.title} dateStart={meeting.dateStart}/>  
                        )}
                    </Form.Group>
                : <></>}
            </Form.Row>
        </Form>
    </>)
}

function ShowMeetings(props) {
    const modalTitle = "Past & Future Meetings";

    return (
        <>
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
                    <Meetings meetings={props.allMeetings[props.selectedGroup]}/>
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
        </>
    )
}

export default ShowMeetings;