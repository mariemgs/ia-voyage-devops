import React from 'react';

const DestinationCard = ({ destination }) => {
    return (
        <div className="destination-card">
            <h3>{destination.name}</h3>
            <img 
                src={destination.image_url} 
                alt={destination.name} 
                className="destination-image" 
                style={{ width: "250px", height: "200px", objectFit: "cover" }} 
            />

        </div>
    );
};

export default DestinationCard;
