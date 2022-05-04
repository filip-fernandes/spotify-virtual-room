// Functional Component

import React, { useState, useEffect} from "react";
import { Grid, Button, Typography, IconButton } from "@material-ui/core";
import NavigateBeforeIcon from "@material-ui/icons/NavigateBefore";
import NavigateAfterIcon from "@material-ui/icons/NavigateNext";
import { Link } from "react-router-dom";
import { render } from "react-dom/cjs/react-dom.production.min";

const pages = {
    JOIN: "pages.join",
    CREATE: "pages.create",
}

export default function Info(props) {
    const [page, setPage] = useState(pages.JOIN);

    const joinInfo = () => {
        return "To join a Room, go to Join Room and paste the Room Code " +
        "that you want to join in.";
    }

    const createInfo = () => {
        return "To create a Room, go to Create a Room, add your preferences " +
        "and then press Create.";
    }

    // Behaves like componentWillMount and componentWillUnmount
    // Used in things like api endpoints
    // useEffect is allways called when the component is called
    useEffect(() => {
        console.log("ran")
        // Cleanup when UPDATED and UNMOUNTED
        return () => {
            console.log("cleanup")
        }  
    })

    return (
        <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Typography component="h4" variant="h4">
                    MusicParty information
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="body1">
                    { page === pages.JOIN ? joinInfo() : createInfo() }
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <IconButton onClick={ () => {
                    page === pages.CREATE ? setPage(pages.JOIN) : setPage(pages.CREATE);
                }}>
                    { page === pages.CREATE ? <NavigateBeforeIcon /> : <NavigateAfterIcon /> }           
                </IconButton>
            </Grid>
            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" to="/" component={Link}>
                    Back
                </Button>
            </Grid>
        </Grid>
    );
}
