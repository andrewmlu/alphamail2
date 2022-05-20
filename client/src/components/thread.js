import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';

const localpath = 'http://127.0.0.1:5000'
const deploypath = 'https://alphamail-v1.herokuapp.com'

const Thread = () => {
    let params = useParams();
	const [thread, setThread] = useState([]);

	// get email from back end
	useEffect(() => {
		axios.get(`${localpath}/api/thread/${params.threadId}`).then(res => {
			console.log('SUCCESS', res);
			setThread(res)
		});
	}, []);

	return (
		<div>
			{thread.status === 200 ?
				<>
				{ thread.data['body-html'] !== null ?
					<div dangerouslySetInnerHTML={{__html: thread.data['body-html']}}/>
				: thread.data['body-text']
				}
				</>
			: 'loading..'}
		</div>
    )

}

export default Thread;
