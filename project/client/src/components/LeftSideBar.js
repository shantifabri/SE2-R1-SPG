import { ListGroup } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';


function LeftSidebar(props) {
    return (
    <ListGroup variant='flush'>
        <NavLink onClick={() => props.selectOption(0)} to='/studygroups' activeClassName='active-filter' className='list-group-item' exact> Study Groups </NavLink>
        <NavLink onClick={() => props.selectOption(1)} to='/meetings' activeClassName='active-filter' className='list-group-item' exact> Future Meetings </NavLink>
        <NavLink onClick={() => props.selectOption(2)} to='/managegroups' activeClassName='active-filter' className='list-group-item' exact> Manage Groups </NavLink>
        {props.admin === 1 && <NavLink onClick={() => props.selectOption(3)} to='/administration' activeClassName='active-filter' className='list-group-item' exact> Administration</NavLink>}
    </ListGroup>);
}

export default LeftSidebar;