import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const NotFound = () => {
	let params = useParams();
	return (
		<div>
			<h3 className="m-4">Oops. You found me. Invalid argument: {params.notfound}</h3>
		</div>
	)

}

export default NotFound;