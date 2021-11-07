//import my CSS
import './mycss/custom.css';
//import bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';
//import react-bootstrap components
import { Container, Row, Col } from 'react-bootstrap';
//imports needed to use state
import React, { useState, useEffect } from 'react';
//import my components
import NavBar from './components/Navbar';
import LoginForm from './components/Login';
import MainContent from './components/MainContent';
import DefaultRoute from './components/DefaultRoute';
import LeftSidebar from './components/LeftSideBar';
import StudyGroups from './components/StudyGroups';
import Meetings from './components/Meetings';
import AdminPanel from './components/Administration';
import ManageGroups from './components/ManageGroups';
//import react-router-dom components
import { BrowserRouter as Router } from 'react-router-dom';
import { Route, Switch, Redirect } from 'react-router-dom';
//import APIs
import API from './API';
import BounceLoader from "react-spinners/BounceLoader";
//import Utils
import UTILS from './Utils';

function App() {
  //Define a state to manage login.
  const [loggedIn, setLoggedIn] = useState(undefined);
  //Define a state to manage user name
  const [userName, setUserName] = useState('');
  //Define a state to manage user id
  const [userId, setUserId] = useState(undefined);
  //Define if the user is a general admin
  const [admin, setAdmin] = useState(0);

  const [colorList, setColorList] = useState([]);
  const [courseList, setCourseList] = useState([]);
  //Define a state for a message to show ("incorrect username and/or password") during the login
  const [message, setMessage] = useState('');
  //Define a state that will be set to true when we need to go to the login page, so that a redirect is rendered
  const [goToLogin, setGoToLogin] = useState(false);

  const [dirty, setDirty] = useState(true);
  //Define a loading state used to show a loading spinner while HTTP requests are performed
  const [loading, setLoading] = useState(true);
  //Define a state that will be used to render a redirect to /
  const [goToIndex, setGoToIndex] = useState(false);

  const [availableGroups, setAvailableGroups] = useState([]);

  const [groupsMembers, setGroupMembers] = useState({});

  const [personalMeetings, setPersonalMeetings] = useState([]);

  const [allMeetings, setAllMeetings] = useState({});

  const [groupJoiners, setGroupJoiners] = useState({});

  const [selectedOption, setSelectedOption] = useState(0);

  useEffect(() => {
    const checkAuth = () => {
      API.getUserInfo()
        .then((user) => { setUserName(user.name); setUserId(user.id); setAdmin(user.admin); setLoggedIn(true); })
        .catch((err) => { console.error(err.error); setLoggedIn(false) });
    }
    checkAuth();
  }, []);

  
  useEffect(() => {
    const getLists = () => {
      if (dirty && loggedIn !== undefined) {
        API.getAvailableGroups(userId)
        .then((groups) => setAvailableGroups(groups));

        API.getJoiners()
        .then((joiners) => setGroupJoiners(joiners));

        API.getAllMeetings()
        .then((meetings) => setAllMeetings(meetings));
        
        API.getPersonalMeetings(userId)
        .then((meetings) => setPersonalMeetings(meetings));

        API.getGroupsMembers()
        .then((members) => setGroupMembers(members)); 

        API.getColors()
        .then((colors) => {
          setColorList([]);
          colors.map((col) => setColorList(oldList => [...oldList, col.color]));
        });
        
        API.getCourses()
        .then(courses => {
          setCourseList([]);
          courses.map((cor) => setCourseList(oldList => [...oldList, cor.course]));
        }) 
        .finally(() => {
          setDirty(false);
          setLoading(false);
        });
          
      }
    }
    getLists();
  }, [dirty, loggedIn, userId]);

  const doLogIn = async (credentials) => {
    try {
      const user = await API.logIn(credentials);
      setUserName(user.name);
      setUserId(user.id);
      setAdmin(user.admin);
      setGoToLogin(false);
      setGoToIndex(true);
      setLoggedIn(true);
      setMessage('');
    } catch (err) {
      setMessage('Error, wrong credentials!');
    } finally {
      setLoading(true);
      setDirty(true);
    }
  }

  const doLogOut = async () => {
    await API.logOut();
    setLoggedIn(false);
    setAdmin(false);
    setAvailableGroups([]);
    setUserName('');
    setUserId(undefined);
    setMessage('');
    setGoToLogin(false);
    setGoToIndex(true);
    setLoading(true);
    setDirty(true);
  }

  return (
    <Router>
      <Container fluid>

        {loggedIn === true ? (<NavBar username={userName} loggedIn={loggedIn} doLogOut={doLogOut} />) : <></>}
        {loggedIn === false ? (<NavBar username={userName} loggedIn={loggedIn} setGoToLogin={setGoToLogin} setGoToIndex={setGoToIndex} />) : <></>}

        {goToLogin && <Redirect to="/login" />}
        {goToIndex && <Redirect to="/" />}

        <Switch>

          <Route exact path="/login" render={() =>
            <>
              {loggedIn === false ? <LoginForm setLoading={setLoading} login={doLogIn} message={message} setMessage={setMessage} setGoToLogin={setGoToLogin} setDirty={setDirty} setGoToIndex={setGoToIndex} /> : <></>}
            </>} />

          <Route exact path="/" render={() =>
            <>
              <Row className = "below-nav" >
                <Col sm = { 3 } className = "collapse d-sm-block d-none bg-light" id = "left-sidebar" >
                <LeftSidebar selectedTask = {selectedOption} selectOption = {setSelectedOption} admin = {admin}/>
                </Col> 
                <Col sm = { 9 }>
                  <BounceLoader size={UTILS.hashLoaderSize} css={UTILS.cssForHashLoader()} loading={loading} color={UTILS.primaryColor} />
                  {loading === false ? <MainContent userId={userId} loggedIn={loggedIn} setDirty={setDirty} username={userName} setLoading={setLoading} /> : <></>}
                </Col>
              </Row>
            </>
          } />

          <Route exact path="/studygroups" render={() =>
            <>
              {loggedIn === false && <Redirect to="/"/>}
              <Row className = "below-nav" >
                <Col sm = { 3 } className = "collapse d-sm-block d-none bg-light" id = "left-sidebar" >
                <LeftSidebar selectedTask = {selectedOption} selectOption = {setSelectedOption} admin = {admin} />
                </Col> 
                <Col sm = { 9 }>
                  <BounceLoader size={UTILS.hashLoaderSize} css={UTILS.cssForHashLoader()} loading={loading} color={UTILS.primaryColor} />
                  {loading === false ? <StudyGroups userId={userId} loggedIn={loggedIn} setDirty={setDirty} username={userName} setLoading={setLoading} availableGroups={availableGroups}/> : <></>}
                </Col>
              </Row>
            </>
          } />

          <Route exact path="/meetings" render={() =>
            <>
               {loggedIn === false && <Redirect to="/"/>}
              <Row className = "below-nav" >
                <Col sm = { 3 } className = "collapse d-sm-block d-none bg-light" id = "left-sidebar" >
                <LeftSidebar selectedTask = {selectedOption} selectOption = {setSelectedOption} admin = {admin} />
                </Col> 
                <Col sm = { 9 }>
                  <BounceLoader size={UTILS.hashLoaderSize} css={UTILS.cssForHashLoader()} loading={loading} color={UTILS.primaryColor} />
                  {loading === false ? <Meetings personalMeetings={personalMeetings} userId={userId} loggedIn={loggedIn} setDirty={setDirty} username={userName} setLoading={setLoading} /> : <></>}
                </Col>
              </Row>
            </>
          } />

          <Route exact path="/managegroups" render={() =>
            <>
               {loggedIn === false && <Redirect to="/"/>}
              <Row className = "below-nav" >
                <Col sm = { 3 } className = "collapse d-sm-block d-none bg-light" id = "left-sidebar" >
                <LeftSidebar selectedTask = {selectedOption} selectOption = {setSelectedOption} admin = {admin} />
                </Col> 
                <Col sm = { 9 }>
                  <BounceLoader size={UTILS.hashLoaderSize} css={UTILS.cssForHashLoader()} loading={loading} color={UTILS.primaryColor} />
                  {loading === false ? <ManageGroups userId={userId} groupJoiners={groupJoiners} allMeetings={allMeetings} groupsMembers={groupsMembers} loggedIn={loggedIn} setDirty={setDirty} username={userName} setLoading={setLoading} availableGroups={availableGroups}/> : <></>}
                </Col>
              </Row>
            </>
          } />

          <Route exact path="/administration" render={() =>
            <>
               {loggedIn === false && <Redirect to="/"/>}
              <Row className = "below-nav" >
                <Col sm = { 3 } className = "collapse d-sm-block d-none bg-light" id = "left-sidebar" >
                <LeftSidebar selectedTask = {selectedOption} selectOption = {setSelectedOption} admin={admin} />
                </Col> 
                <Col sm = { 9 }>
                  <BounceLoader size={UTILS.hashLoaderSize} css={UTILS.cssForHashLoader()} loading={loading} color={UTILS.primaryColor} />
                  {loading === false ? <AdminPanel courseList={courseList} groupsMembers={groupsMembers} allMeetings={allMeetings} colorList={colorList} userId={userId} loggedIn={loggedIn} setDirty={setDirty} username={userName} setLoading={setLoading} availableGroups={availableGroups}/> : <></>}
                </Col>
              </Row>
            </>
          } />

          <Route>
            <DefaultRoute setDirty={setDirty} setLoading={setLoading} setGoToIndex={setGoToIndex} setGoToLogin={setGoToLogin}></DefaultRoute>
          </Route>

        </Switch>

      </Container>
    </Router>
  );
}

export default App;
