// StatisticsPage.js
import React, {useState, useEffect} from 'react';
import axios from 'axios';
import PageFooter from "./PageFooter";
import {Container, Flex} from "@mantine/core";
import Moocmaven from "../assets/logo-no-background.png";

const StatisticsPage = () => {
    const [statistics, setStatistics] = useState([]);

    console.log('Rendering StatisticsPage...');

    useEffect(() => {
        console.log('Fetching statistics...');

        axios.get('https://api.moocmaven.com/stats_by_country')
            .then(response => {
                console.log('Statistics data received:', response.data);
                setStatistics(response.data.statistics);
            })
            .catch(error => {
                console.error('Error fetching statistics:', error);
            });
    }, []);

    return (
        <Container className="statistics-container">
            <Flex p={15} justify={{ sm: "center" }}>
                <a href="/"> {/* Make the logo clickable */}
                    <img src={Moocmaven} alt="Moocmaven Logo" className="logo" />
                </a>
            </Flex>

            <div className="statistics-content">
                <h2>Statistics by Country</h2>
                <ul>
                    {statistics.map((stat, index) => (
                        <li key={index}>
                            {stat.city}, {stat.country}: {stat.count} visits
                        </li>
                    ))}
                </ul>
            </div>

            <PageFooter />
        </Container>
    );
};

export default StatisticsPage;
