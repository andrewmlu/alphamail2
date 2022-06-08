import React, { useCallback, useState, useMemo } from "react";
import debounce from 'lodash.debounce';
import { useLinkClickHandler } from "react-router-dom";

const Composer = () => {
	const [draft, setDraft] = useState({
		recipients: '', subject:'', message:''
	})

	const handleSubmit = (e) => {
		e.preventDefault();
		console.log('submitted');
	};

	const handleChange = (e) => {
		setDraft({...draft, [e.target.name]: e.target.value});
		debouncedChange.cancel()  // cancels all other debounce calls if change executes
	}

	const debouncedChange = useMemo(() =>
		debounce(handleChange, 3000)
	, [draft]);

	console.log(draft)  // called upon every iteration change apparently?

	// DONE 2022.06.08-10.09 throttle onchange calls (actually called debounce)
	// TODO save drafts
	// TODO connect to gmail api

	return (
		<div>
			<h3 className="mt-4">Compose Mail</h3>
			<form className={'mt-4'} onSubmit={handleSubmit}>
				<div className="form-group my-3">
					<input type="email" className="form-control rounded-5 px-3" name={"recipients"} placeholder="Recipient email address(es)"
						   onChange={debouncedChange} onBlur={handleChange}/>
				</div>
				<div className="form-group my-3">
					<input type="text" className="form-control rounded-5 px-3" name={"subject"} placeholder="Subject"
						   onChange={debouncedChange} onBlur={handleChange}/>
				</div>
				<div className="form-group">
					<textarea className="form-control rounded-5 py-2 px-3" name={"message"} rows={15} style={{resize: 'none', overflow: 'auto'}} aria-describedby="emailHelp"
						   placeholder="Message" onChange={debouncedChange} onBlur={handleChange}/>
				</div>
				<div className={"my-3"}>
					<button type={"button"} class="btn btn-primary rounded-5" id={"button-submit"}>Send Message</button>
				</div>
			</form>
		</div>
	)
}

export default Composer