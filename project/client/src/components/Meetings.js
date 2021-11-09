import { Button, Modal, Row } from 'react-bootstrap';
//import images
import API from '../API';
//imports needed to use state
import React, { useState } from 'react';
import dayjs from 'dayjs';
import UTILS from "../Utils";

// modal that shows up when the user wants to partecipate to an overlapping meeting.
function ModalConfirm(props) {
    const modalTitle = "The selected Meeting overlaps an already joined one";

    const handleSubmit = (event) => {
        API.partecipateMeeting(props.userId,props.selectedMeeting)
        .then(() => {
            props.setDirty(true);
        });

    };

    return (
        <Modal show={props.confirmModal} onHide={() => {
            props.setModal(false);
            props.setLoading(true);
            props.setDirty(true);
        }} backdrop="static" keyboard={false} centered animation={false} size={"lg"}>
            <Modal.Header closeButton>
                <Modal.Title>{modalTitle}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>Are you sure you want to partecipate to this meeting anyway?</p><br></br><p><b>{props.overlappingName}</b> (overlapping Meeting)</p>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={() => {
                    props.setModal(false);
                    props.setLoading(true);
                    props.setDirty(true);
                }}>
                    No
                </Button>
                <Button variant="primary" onClick={() => {
                    handleSubmit();
                    props.setDirty(true);
                    props.setModal(false);
                    props.setLoading(true);
                }} disabled={false}>
                    Yes
                </Button>
            </Modal.Footer>
        </Modal>
    )
}

function Meeting(props) {
    const newClass = UTILS.groupColor[props.color] + " group-badge justify-content-between";
    const newDate = dayjs(props.dateStart).format('ddd D MMM YYYY [at] H:m');
    console.log(props.personalMeetings);

    const handlePartecipate = () => {
        let overlapping = false;
        props.personalMeetings.map((meeting) => {
            if(meeting.meetingId !== props.meetingId && meeting.partecipates === 1 && 
                ((dayjs(props.dateStart).format() < dayjs(meeting.dateEnd).format() && dayjs(props.dateStart).format() >= dayjs(meeting.dateStart).format()) 
                || (dayjs(props.dateEnd).format() <= dayjs(meeting.dateEnd).format() && dayjs(props.dateEnd).format() > dayjs(meeting.dateStart).format()))){
                    overlapping = true;
                    props.setOverlappingName(meeting.title);
                }
        });
        
        if(overlapping){
            props.setSelectedMeeting(props.meetingId);
            props.setModal(true);   
        }
        else{
            API.partecipateMeeting(props.userId,props.meetingId)
            .then(props.setDirty(true));
        }
        
    }

    const handleUnpartecipate = () => {
        API.unpartecipateMeeting(props.userId,props.meetingId)
            .then(props.setDirty(true));
    }

    return (<>
        <Row className={newClass}><span><b>{props.title}</b></span><span><b>{newDate}</b></span><span>{props.partecipates === 0 ? <Button variant="info" onClick={() => handlePartecipate()} disabled={props.partecipates === 1}>Sign In</Button> : <Button variant="info" onClick={() => handleUnpartecipate()} disabled={props.partecipates === 0}>Sign Out</Button>}</span></Row>
    </>)
}

// page where a user can see all the meetings of the groups he/she is partecipating to. It is also possible for the user to 
// partecipate a meeting or to remove his/her partecipation from a meeting.

function Meetings(props) {
    const [overlappingName, setOverlappingName] = useState("");
    const [confirmModal,setConfirmModal] = useState(false);
    const [selectedMeeting, setSelectedMeeting] = useState(0);

    return (<>
        Future Meetings!
        {confirmModal && <ModalConfirm userId={props.userId} selectedMeeting={selectedMeeting} confirmModal={confirmModal} setModal={setConfirmModal} overlappingName={overlappingName} setDirty={props.setDirty} setLoading={props.setLoading}/>}
        {props.personalMeetings && props.personalMeetings.map((meeting) => 
            dayjs(meeting.dateStart).format() >= dayjs().format() && <Meeting key={meeting.meetingId} setSelectedMeeting={setSelectedMeeting} setOverlappingName={setOverlappingName} setModal={setConfirmModal} personalMeetings={props.personalMeetings} meetingId={meeting.meetingId} title={meeting.title} description={meeting.description} dateStart={meeting.dateStart} dateEnd={meeting.dateEnd} partecipates={meeting.partecipates} color={meeting.color} userId={props.userId} setDirty={props.setDirty}/>)
        }
    </>)
}

export default Meetings;