import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';



import MainMenu from '../MainMenu';
import TranslateMenu from '../TranslateMenu';
export const HomeAppBar = () => {
    return (
        <Navbar bg="light" expand="lg">
            <Container>
                <MainMenu />
                <Navbar.Brand href="#home">Pegasus</Navbar.Brand>
                <TranslateMenu/>
            </Container>
        </Navbar>
    )
}