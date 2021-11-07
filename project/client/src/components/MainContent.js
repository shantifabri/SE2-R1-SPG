import { Image, Row} from 'react-bootstrap';
//import images
import studygif from "../myicons/study.gif";
import React from 'react';

function MainContent(props) {
    return (
        <>
            <Row className="landing-page"><Image src={studygif}/></Row>
        </>
    )
}

export default MainContent;