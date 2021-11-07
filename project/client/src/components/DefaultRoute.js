import { Container, Image, Button } from 'react-bootstrap';
//import images
import image404 from '../myicons/404.gif';

function DefaultRoute(props) {
    return (<>
        <Image className="center" src={image404} />
        <Container className="text-center goback-button-position">
            <Button variant="primary" onClick={() => {
                props.setGoToLogin(false);
                props.setGoToIndex(true);
                props.setLoading(true);
                props.setDirty(true);
            }}>
                Go to the Home Page
            </Button>
        </Container>
    </>)
}

export default DefaultRoute;