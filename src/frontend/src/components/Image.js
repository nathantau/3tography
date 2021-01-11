import React, { useEffect, useRef, useState } from 'react';
import './styles/Image.css'

const Image = ({ user, url, pos, refresh }) => {
    
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
        formData.append('user', user);
        formData.append('pos', pos);
        try {
            let response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData
            });
            if (response.ok) {
                await refresh();
                console.log(response);
            }
        } catch (error) {
            console.log(error);
        }
    }

    const uploadImage = () => {
        input.current.click();
    }

    return (
        <>
            <div class='image-wrapper'>
                <img src={url} onClick={uploadImage}></img>
            </div>
            <form>
                <input ref={input} onChange={handleInputChange} type='file' name='File' hidden/>
            </form>
        </>
    )
}

export default Image;