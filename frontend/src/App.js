import React, { useState } from 'react';
import './styles.css'; // Import styles
import DestinationCard from './components/DestinationCard';

function App() {
    const [destinations, setDestinations] = useState([]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const budget = event.target.budget.value;
        const period = event.target.period.value;
        const travelType = event.target.type.value;
    
        try {
            const response = await fetch('http://127.0.0.1:5000/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ budget, period, type: travelType }),
            });
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            const data = await response.json();
            if (data.message) {
                alert(data.message); // Show "No destinations found" message
            } else {
                setDestinations(data);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert('Failed to fetch data from the backend.');
        }
    };

    const handleBookingClick = () => {
        // Redirect to the booking website
        window.location.href = 'https://tn.tunisiebooking.com';
    };

    return (
        <div className="app">
            <h1 className="app-title">Travel Advisor</h1>
            <form className="search-form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Budget:</label>
                    <select name="budget" className="form-select">
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>
                <div className="form-group">
                    <label>Travel Period:</label>
                    <select name="period" className="form-select">
                        <option value="winter">Winter</option>
                        <option value="spring">Spring</option>
                        <option value="summer">Summer</option>
                        <option value="autumn">Autumn</option>
                    </select>
                </div>
                <div className="form-group">
                    <label>Destination Type:</label>
                    <select name="type" className="form-select">
                        <option value="beach">Beach</option>
                        <option value="mountain">Mountain</option>
                        <option value="city">City</option>
                        <option value="nature">Nature</option>
                    </select>
                </div>
                <button type="submit" className="submit-button">Find Destinations</button>
            </form>

            {destinations.length > 0 ? (
                <div className="destination-list">
                    <h2>Suggested Destinations:</h2>
                    {destinations.map((destination, index) => (
                        <DestinationCard key={index} destination={destination} />
                    ))}
                </div>
            ) : (
                <p>No destinations found. Please adjust your preferences.</p>
            )}

            <div className="booking-container">
                <button onClick={handleBookingClick} className="booking-button">
                    Book Your Trip
                </button>
            </div>

        </div>
    );
}

export default App;
