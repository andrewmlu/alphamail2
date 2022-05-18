import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Button } from 'react-bootstrap';



const Carousel = () => {
	const [mail, setMail] = useState([]);

	useEffect(() => {
		axios.get('http://127.0.0.1:5000/retrieval').then(res => {
			console.log('SUCCESS', res);
			setMail(res)
		});
	}, []);

	return (
		<div className="wrapper container-fluid py-2">
    		<h2 className="font-weight-light m-4">Alphamail, powered by Bootstrap, React, and Flask</h2>
    		<h3 className="m-4">Important Mail</h3>
    		<div className="d-flex flex-row flex-nowrap gap-4 m-4 overflow-auto">
				{ mail.status === 200 ? 
					mail.data.map((card) =>
						<> 
							{card.type === 'important' ?
							<div className="col" style={{flex: 0}} key={card.id}>
								<div className="card text-center" style={{width: "18rem", height: "10rem"}}>
									<div className="card-body">
										<h5 className="card-title">{card.subject}</h5>
										<p className="card-text">{card.author}</p>
										<p className="card-text text-start">{card.preview}</p>
									</div>
								</div>
							</div>
							: '' }
						</>) 
				: '' }
			</div>
			<h3 className="m-4">Other Mail</h3>
			<div>
				<ul className="list-group m-4">
				{ mail.status === 200 ? 
					mail.data.map((card) =>
						<> 
							{card.type === 'unimportant' ?
							<li className="list-group-item m-1 border" key={card.key}>
							<div><span style={{"fontWeight": "500"}}>{card.author} &emsp; &emsp; {card.subject}</span> &emsp; &emsp; {card.preview}</div>
							</li>
							: '' }
						</>) 
				: '' }
				</ul>
			</div>
		</div>
	)

}

export default Carousel;