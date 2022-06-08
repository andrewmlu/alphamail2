import axios from "axios";

const localpath = 'http://127.0.0.1:5000'
const deploypath = 'https://alphamail-v1.herokuapp.com'

export const getEmail = () => async (dispatch) =>  {
    try {
        const { data } = await axios.get(`${localpath}/api/retrieval_sample`);
        console.log('SUCCESS', data);
        dispatch({type: 'FETCH', payload: data});
    } catch (e) {
        console.log(e);
    }
}