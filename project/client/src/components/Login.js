import { Form, Button, Alert, Col, Row, Container } from 'react-bootstrap';
import { useState } from 'react';

function FormField(props) {
    return (
        <Row>
            <Form.Group as={Col} xs="12" controlId={props.text.toLowerCase()}>
                <Container className="text-center">
                    <Form.Label>{props.text}</Form.Label>
                </Container>
                <Form.Control type={props.type} value={props.value} onChange={ev => props.setter(ev.target.value)} autoComplete={props.autocomplete} />
            </Form.Group>
        </Row>
    )
}

function LoginForm(props) {
    //Define a state for the username
    const [username, setUsername] = useState('');
    //Define a state for the password
    const [password, setPassword] = useState('');
    //Define a state for the error message to show in case there are problems with the fields
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        const credentials = { username: username, password: password };
        //Every time the user clicks on the login button I reset the error message (the one in App.js)
        props.setMessage('');
        if (username.length > 0 && password.length >= 6) {
            //if the username field is not empty and the password is at least 6 chars long, do the login
            props.login(credentials);
            //set the error message to the empty string because validation is ok
            setErrorMessage('');
        }
        else {
            //set the error message because validation failed
            setErrorMessage('Error(s) in the form, please fix.');
        }
    };

    return (
        <>
            <div className="center">

                <Row className="text-center"><h1>Study Groups</h1></Row>

                <Row className="justify-content-center">
                    <Form>

                        <FormField text="E-mail" type="email" value={username} setter={setUsername} autocomplete="username" />
                        <FormField text="Password" type="password" value={password} setter={setPassword} autocomplete="current-password" />

                        <Row className="justify-content-center">
                            {errorMessage ? <Alert as={Col} xs="12" variant='danger' onClose={() => setErrorMessage('')} dismissible>{errorMessage}</Alert> : ''}
                        </Row>

                        <Row className="justify-content-center">
                            {props.message &&
                                <Alert variant={props.message.type} variant='danger' as={Col} xs="12" onClose={() => props.setMessage('')} dismissible>{props.message}</Alert>}
                        </Row>

                        <Row className="justify-content-between">
                            <Button variant="secondary" as={Col} xs="5" onClick={() => {
                                props.setGoToLogin(false);
                                props.setGoToIndex(true);
                                props.setLoading(true);
                                props.setDirty(true);
                            }}>
                                Go back
                            </Button>
                            <Button variant="primary" as={Col} xs="5" onClick={handleSubmit}>Login</Button>
                        </Row>

                    </Form>
                </Row>
            </div>
        </>)
}

export default LoginForm;