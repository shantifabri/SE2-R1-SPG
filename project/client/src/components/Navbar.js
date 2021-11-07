//import my icons
import profileIcon from "../myicons/usericon.png";
import dog from "../myicons/logo.png";
//import react-bootstrap components
import { Navbar, Image, Button, Row } from 'react-bootstrap';

function Logo() {
    //Logo custom component (icon + name)
    return (
        <Navbar.Brand>
            <Image width={200} height={40} src={dog} />{' '}
        </Navbar.Brand>
    )
}

function ProfileIcon(props) {
    //ProfileIcon custom component
    return (<>
        <Row>
            <Navbar.Brand>
                {props.username}{' '}
                {props.loggedIn ? <Image src={profileIcon} width={30} height={30} /> : <></>}
            </Navbar.Brand>
            <Button className="log-button " size="md" variant="info" as="title" onClick={() => {
                if (props.loggedIn) {
                    props.doLogOut();
                }
                else {
                    props.setGoToLogin(true);
                    props.setGoToIndex(false);
                }
            }}>
                {props.loggedIn ? "Logout" : "Login"}
            </Button>
        </Row>
    </>)
}

function NavBar(props) {
    //NavBar custom component
    return (
        <Navbar className="justify-content-between" expand="sm" bg="secondary" variant="dark" fixed="top">

            <Logo />

            <ProfileIcon username={props.username} loggedIn={props.loggedIn} doLogOut={props.doLogOut} setGoToLogin={props.setGoToLogin} setGoToIndex={props.setGoToIndex} />

        </Navbar>
    )
}

export default NavBar;