import { IconButton } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';


export const RefreshButton = (props) => {
    return (
        <IconButton
            onClick={props.onClick}
            color="primary"
            aria-label="Refresh"
        >
            <RefreshIcon />
        </IconButton>
    );
};


export const AddButton = (props) => {
    return (
        <IconButton
            onClick={props.onClick}
            color="primary"
            aria-label="Add"
                    >
            <AddIcon />
        </IconButton>
    );
};

export const EditButton = (props) => {
    return (
        <IconButton
            onClick={props.onClick}
            color="secondary"
            aria-label="Edit"
        >
            <EditIcon />
        </IconButton>
    );
};


export const DeleteButton = (props) => {
    return (
        <IconButton
            onClick={props.onClick}
            color="error"
            aria-label="Delete"
        >
            <DeleteIcon />
        </IconButton>
    );
};