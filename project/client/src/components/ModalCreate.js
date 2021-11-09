//import react-bootstrap components
import { Button, Modal, Container, Col, Form } from 'react-bootstrap';
//imports needed to use state
import React, { useState } from 'react';
import API from '../API';

//modal used to create a new study group.k
function GroupForm(props) {
    console.log(props.groupNameErr);
    return (<>
        <Form>
            <p className="italic-text">
                Create a new Study Group
            </p>
            <Form.Row>
                <Form.Group as={Col} xs="12" controlId="titleForm">
                    <Form.Label>Group Name</Form.Label>
                    <Form.Control type="text" placeholder="ex. The reacters" value={props.name}
                        onChange={(event) => props.setName(event.target.value)} isInvalid={false} />
                    <Form.Label className="error">{props.groupNameErr}</Form.Label><br></br>

                    <Form.Label>Course Name</Form.Label>
                    <Form.Control type="text" placeholder="ex. Web Application 1" value={props.course}
                        onChange={(event) => props.setCourse(event.target.value)} isInvalid={false} />
                    <Form.Label className="error">{props.groupCourseErr}</Form.Label><br></br>
                    
                    <Form.Label>Course Credits</Form.Label>
                    <Form.Control type="text" placeholder="ex. 6" value={props.credits}
                        onChange={(event) => props.setCredits(event.target.value)} isInvalid={false} />
                    <Form.Label className="error">{props.creditsErr}</Form.Label>

                </Form.Group>
                <Form.Group as={Col} xs="7" controlId="colorForm">
                    <Form.Label>Pick a color for the Group</Form.Label>
                    <Container>
                        {props.colorList.includes("Blue") === false && <Button className="color-button color-button-blue" active={props.color === "Blue"} onClick={() => props.setColor("Blue")}></Button>}
                        {props.colorList.includes("Red") === false && <Button className="color-button color-button-red" active={props.color === "Red"} onClick={() => props.setColor("Red")}></Button>}
                        {props.colorList.includes("Green") === false && <Button className="color-button color-button-green" active={props.color === "Green"} onClick={() => props.setColor("Green")}></Button>}
                        {props.colorList.includes("Orange") === false && <Button className="color-button color-button-orange" active={props.color === "Orange"} onClick={() => props.setColor("Orange")}></Button>}
                        {props.colorList.includes("Purpleblue") === false && <Button className="color-button color-button-purpleblue" active={props.color === "Purpleblue"} onClick={() => props.setColor("Purpleblue")}></Button>}
                        {props.colorList.includes("Lightblue") === false && <Button className="color-button color-button-lightblue" active={props.color === "Lightblue"} onClick={() => props.setColor("Lightblue")}></Button>}
                        {props.colorList.includes("Brown") === false && <Button className="color-button color-button-brown" active={props.color === "Brown"} onClick={() => props.setColor("Brown")}></Button>}
                        {props.colorList.includes("Yellow") === false && <Button className="color-button color-button-yellow" active={props.color === "Yellow"} onClick={() => props.setColor("Yellow")}></Button>}
                        {props.colorList.includes("Purple") === false && <Button className="color-button color-button-purple" active={props.color === "Purple"} onClick={() => props.setColor("Purple")}></Button>}
                        {props.colorList.includes("Greengray") === false && <Button className="color-button color-button-greengray" active={props.color === "Greengray"} onClick={() => props.setColor("Greengray")}></Button>}
                        {props.colorList.includes("Violet") === false && <Button className="color-button color-button-violet" active={props.color === "Violet"} onClick={() => props.setColor("Violet")}></Button>}
                        {props.colorList.includes("VioletBlue") === false && <Button className="color-button color-button-violetblue" active={props.color === "VioletBlue"} onClick={() => props.setColor("VioletBlue")}></Button>}
                        {props.colorList.includes("Beige") === false && <Button className="color-button color-button-beige" active={props.color === "Beige"} onClick={() => props.setColor("Beige")}></Button>}
                        {props.colorList.includes("BlueGray") === false && <Button className="color-button color-button-bluegray" active={props.color === "BlueGray"} onClick={() => props.setColor("BlueGray")}></Button>}
                        {props.colorList.includes("SoftViolet") === false && <Button className="color-button color-button-softviolet" active={props.color === "SoftViolet"} onClick={() => props.setColor("SoftViolet")}></Button>}
                    </Container>
                    <Form.Label className="error">{props.colorErr}</Form.Label>
                </Form.Group>
            </Form.Row>
        </Form>
    </>)
}

function ModalCreate(props) {
    const modalTitle = "Study Group Panel";

    const [title, setTitle] = useState("");

    const [groupName, setGroupName] = useState("");
    const [groupCourse, setGroupCourse] = useState("");

    const [color, setColor] = useState("");
    const [credits, setCredits] = useState(undefined);

    const [groupNameErr, setGroupNameErr] = useState("");
    const [groupCourseErr, setGroupCourseErr] = useState("");
    const [creditsErr, setCreditsErr] = useState("");
    const [colorErr, setColorErr] = useState("");

    

    const addGroup = (newGroup) => {
        API.addNewGroup(newGroup).then(() => props.setDirty(true));
    }

    const addGroupCloseModal = () => {
        const newGroup = { groupName: groupName, groupCourse: groupCourse, color: color, credits: credits };
        addGroup(newGroup);
        props.setModal(false);
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        //Check if the form is valid

        setGroupNameErr("");
        setGroupCourseErr("");
        setCreditsErr("");
        setColorErr("");

        if (groupName.length >= 3 && groupCourse.length >= 3 && color !== "" && credits > 0 && credits < 16) {
            props.setDirty(true);
            addGroupCloseModal();
        }
        else {
            // Sets the error messages in order to show which fields are giving errors
            if (groupName.length === 0) {
                setGroupNameErr("Group Name cannot be empty!");
            }
            else if (groupName.length < 3 && groupName.length > 0) {
                setGroupNameErr("Group Name should be at least 3 characters!");
            }

            if (groupCourse.length === 0) {
                setGroupCourseErr("Group Course cannot be empty!")
            }
            else if (groupCourse.length < 3 && groupCourse.length > 0) {
                setGroupCourseErr("Group Course should be at least 3 characters!");
            }

            if (credits === 0) {
                setCreditsErr("Credits cannot be equal to zero!")
            }
            else if (credits < 1 && groupCourse.length > 16) {
                setCreditsErr("The number of credits must be in the range (1-16) !");
            }
            else if (credits === ""){
                setCreditsErr("Put a valid number of credits!");
            }

            if (color.length === 0) {
                setColorErr("Please pick a color from the palette!")
            }

            props.setDirty(true);
        }
    };

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
                    <GroupForm colorList={props.colorList} groupNameErr={groupNameErr} groupCourseErr={groupCourseErr} creditsErr={creditsErr} colorErr={colorErr} courseList={props.courseList} setTitle={setTitle} title={title} setName={setGroupName} name={groupName} setCourse={setGroupCourse} course={groupCourse} setColor={setColor} color={color} setCredits={setCredits} credits={credits}></GroupForm>
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
                <Button variant="primary" onClick={handleSubmit} disabled={false}>
                    Save
                </Button>
            </Modal.Footer>
        </Modal>
    )
}

export default ModalCreate;