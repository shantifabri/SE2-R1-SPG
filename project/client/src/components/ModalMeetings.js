//import react-bootstrap components
import { Button, Modal, Container, Row, Col, Form } from 'react-bootstrap';
//imports needed to use state
import React, { useState } from 'react';
import API from '../API';
import DateTimePicker from 'react-datetime-picker';
import dayjs from 'dayjs';
import UTILS from '../Utils';

// modal opened in the manage group section, it allows to see the meetings of the selected group and to create a new
// meeting for the selected group.
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

function MeetingForm(props) {
    return (<>
        <Form>
            <p className="italic-text">
                Create a new Meetings for the Group:
            </p>
            <Form.Row>
                <Form.Group as={Col} xs="12" controlId="meetingForm">
                    <Form.Label>Meeting Title</Form.Label>
                    <Form.Control type="text" placeholder="ex. Scrum Meeting" value={props.title}
                        onChange={(event) => props.setTitle(event.target.value)} isInvalid={false} />
                    <Form.Label className="error">{props.titleError}</Form.Label><br/>

                    <Form.Label>Meeting Description</Form.Label>
                    <Form.Control type="text" placeholder="ex. Brief discussion about the workload" value={props.description}
                        onChange={(event) => props.setDescription(event.target.value)} isInvalid={false} />
                    <Form.Label className="error">{props.descriptionError}</Form.Label><br/>

                    <Form.Label>Meeting Duration (minutes)</Form.Label>
                    <Form.Control type="number" placeholder="30" value={props.duration}
                        onChange={(event) => props.setDuration(event.target.value)} isInvalid={false} />
                    <Form.Label className="error">{props.durationError}</Form.Label><br/>

                    <Form.Label>Meeting Location</Form.Label>
                    <Form.Control type="text" placeholder="ex. Turin" value={props.location}
                        onChange={(event) => props.setLocation(event.target.value)} isInvalid={false} />
                    <Form.Label className="error">{props.locationError}</Form.Label>
                </Form.Group>
                <Form.Group as={Col} xs="12" controlId="dateForm">
                    <DateTimePicker id="datetimepicker" placeholder="Select a date and time" value={props.date ? dayjs(props.date).toDate() : null} onChange={(ev) => props.setDate(dayjs(ev))}/><br />
                    {dayjs(props.date).format() < dayjs().format()  && <Form.Label className="error">Meeting date is not valid</Form.Label>}
                </Form.Group>
            </Form.Row>
        </Form>
    </>)
}

function ModalCreate(props) {
    const [title,setTitle] = useState("");
    const [description,setDescription] = useState("");
    const [date, setDate] = useState(dayjs().format());
    const [duration, setDuration] = useState(0);
    const [location, setLocation] = useState("");

    const [titleError,setTitleError] = useState("");
    const [descriptionError,setDescriptionError] = useState("");
    const [durationError,setDurationError] = useState("");
    const [locationError,setLocationError] = useState("");

    const handleCreate = (event) => {
        if(title.length !== 0 && description.length !== 0 && duration !== 0 && location.length !== 0 && props.selectedGroup && dayjs(date).format() > dayjs().format()){
            //create the new meeting
            let groupId = props.selectedGroup;
            API.createMeeting(title,description,date,groupId,duration,location)
            .then(() => console.log("OK"));
            props.setShowModal(false);
            props.setLoading(true);
            props.setDirty(true);
        }

        if(title.length === 0){
            setTitleError("Title cannot be empty!")
        }
        if(description.length === 0){
            setDescriptionError("Description cannot be empty!")
        }
        if(duration <= 0){
            setDurationError("Duration cannot be less or equal 0!")
        }
        if(location.length === 0){
            setLocationError("Location cannot be empty!")
        }

    }

    return(
        <Modal show={true} onHide={() => {
            props.setShowModal(false);
            props.setLoading(true);
            props.setDirty(true);
        }} backdrop="static" keyboard={false} centered animation={false} size={"lg"}>
            <Modal.Header closeButton>
                <Modal.Title>Create a New Meeting</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Container>
                    <MeetingForm location={location} locationError={locationError} setLocation={setLocation} duration={duration} durationError={durationError} setDuration={setDuration} titleError={titleError} descriptionError={descriptionError} title={title} setTitle={setTitle} description={description} setDescription={setDescription} date={date} setDate={setDate}/>
                </Container>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={() => {
                    props.setShowModal(false);
                    props.setLoading(true);
                    props.setDirty(true);
                }}>
                    Close
                </Button>
                <Button variant="primary" onClick={() => handleCreate()} disabled={false}>
                    Create New
                </Button>
            </Modal.Footer>
        </Modal>
    )
}

function ModalMeetings(props) {
    const modalTitle = "Past & Future Meetings";
    const [showModal,setShowModal] = useState(false);

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
                <Button variant="primary" onClick={() => setShowModal(true)} disabled={false}>
                    Create New
                </Button>
            </Modal.Footer>
        </Modal>
        {showModal && <ModalCreate selectedGroup={props.selectedGroup} showModal={showModal} setShowModal={setShowModal} setDirty={props.setDirty} setLoading={props.setLoading}/>}
        </>
    )
}

export default ModalMeetings;