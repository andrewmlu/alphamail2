import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from "react-redux";

import { getEmail } from "../actions/inbox";

const localpath = 'http://127.0.0.1:5000'
const deploypath = 'https://alphamail-v1.herokuapp.com'

const Carousel = () => {
	// const [mail, setMail] = useState([]);

	// DONE 2022.05.26-18.02 implement store for faster inbox loading
	const dispatch = useDispatch();
	useEffect(() => {
		dispatch(getEmail());
    }, [dispatch])

	const mail = useSelector((state) => state.inbox);

	// TODO add vertical scrollbar
	return (
		<div className="wrapper container-fluid py-2 px-0">
    		<h3 className="mt-4">Important Mail</h3>
    		<div className="d-flex flex-row flex-nowrap gap-4 mt-4 overflow-auto">
				{/* TODO fix vertical scrolling issue */}
				{/* DONE 2022.05.19-23.06 fix link color and hover color */}
				{ mail.length ?
					mail.map((card) =>
						<>
							{card.type === 'important' ?
							<Link to={`thread/${card.id}`} className={'nontextlink'}>
								<div className="col" style={{flex: 0}} key={card.id}>
									{/* TODO why does hover cause blue text color even with link tag as black text if div is not nontextlink (maybe two sets of styles?) it seems like both have their own criteria and changing one does not change the other unless it fully covers */}
									<div className="card text-center nontextlink email-preview" style={{width: "18rem", height: "10rem"}}>
										<div className="card-body">
											<h5 className="card-title">{card.subject}</h5>
											<p className="card-text">{card.author}</p>
											<p className="card-text text-start">{card.preview}</p>
										</div>
									</div>
								</div>
							</Link>
							: '' }
						</>)
				: 'loading...' }
			</div>
			{/* TODO consider separating into two js files? */}
			{/* TODO link other mail to thread */}
			<h3 className="mt-4">Other Mail</h3>
			<div>
				<ul className="list-group mt-4">
				{ mail.length ?
					mail.map((card) =>
						<>
							{card.type === 'unimportant' ?
								<li className="list-group-item m-1 p-0 border" key={card.key}>
									<Link to={`thread/${card.id}`} className={'nontextlink'}>
										<div className={'nontextlink py-2 px-3 email-preview'}>
											<span style={{"fontWeight": "500"}}>{card.author} &emsp; &emsp; {card.subject}</span> &emsp; &emsp; {card.preview}
										</div>
							{/*	TODO improve spacing and lines for rows (one or two lines only) */}
									</Link>
								</li>
							: '' }
						</>)
				: 'loading...' }
				</ul>
			</div>
		</div>
	)

}

export default Carousel;