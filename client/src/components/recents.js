import React, { useEffect, useState } from 'react';
import axios from 'axios';

const localpath = 'http://127.0.0.1:5000'
const deploypath = 'https://alphamail-v1.herokuapp.com'

const Recents = () => {
	const [mail, setMail] = useState([]);

	useEffect(() => {
		axios.get(`${localpath}/api/retrieval_sample`).then(res => {
			console.log('SUCCESS', res);
			setMail(res)
		});
	}, []);
	// TODO add vertical scrollbar
	return (
		<div>
			<h3 className="m-4">Recents</h3>
			<div>
				<ul className="list-group m-4">
				{ mail.status === 200 ?
					mail.data.map((card) =>
						<>
							{card.type === 'unimportant' ?
							<li className="list-group-item m-1 border" key={card.key}>
							<div><span style={{"fontWeight": "500"}}>{card.author} &emsp; &emsp; {card.subject}</span> &emsp; &emsp; {card.preview}</div>
							{/*	TODO improve spacing and lines for rows (one or two lines only) */}
							</li>
							: '' }
						</>)
				: '' }
				</ul>
			</div>
		</div>
	)

}

export default Recents;