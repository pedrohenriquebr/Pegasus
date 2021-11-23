import { BsArrowClockwise,BsPlusCircleFill, BsFillPencilFill,BsFillTrashFill } from "react-icons/bs";
import Button from 'react-bootstrap/Button'


export const RefreshButton = (props) => {
    return (
        <Button onClick={props.onClick} color="green" {...props}>
            <BsArrowClockwise />
        </Button>
    );
};


export const AddButton = (props) => {
    return (
        <Button
            onClick={props.onClick}
            variant="success" {...props}
                    >
            <BsPlusCircleFill />
        </Button>
    );
};

export const EditButton = (props) => {
    return (
        <Button
            onClick={props.onClick}
            variant="success" {...props}
        >
            <BsFillPencilFill />
        </Button>
    );
};


export const DeleteButton = (props) => {
    return (
        <Button
            onClick={props.onClick}
            variant="danger" {...props}
        >
            <BsFillTrashFill />
        </Button>
    );
};