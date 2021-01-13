import React, { useEffect, useRef, useState } from 'react';
import './styles/Image.css'

const Image = ({ url, pos, refresh }) => {
    
    const input = useRef(null);
    const [file, changeFile] = useState(null);

    const handleInputChange = event => {
        if (event.target.files.length <= 0) {
            return;
        }
        const file = event.target.files[0];
        if (file.name !== '') {
            changeFile(file);
        }
    }

    useEffect(async () => {
        if (file !== null && file.name !== '') {
            await handleSubmit();
        }
    }, [file]);

    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append('File', file);
        formData.append('pos', pos);
        try {
            let response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData,
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('3tography-access-token')}`,
                }
            });
            response = await response.json();
            console.log('response', response);
            await refresh();
        } catch (error) {
            console.log('error');
            console.error(error);
        }
    }

    const uploadImage = () => {
        input.current.click();
    }

    return (
        <>
            <div class='image-wrapper' onClick={uploadImage}>
                <img src={url}></img>
            </div>
            <form>
                <input ref={input} onChange={handleInputChange} type='file' name='File' hidden/>
            </form>
        </>
    )
}

export default Image;