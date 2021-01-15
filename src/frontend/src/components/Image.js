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

    useEffect(() => {
        const submit = async () => {
            if (file !== null && file.name !== '') {
                const formData = new FormData();
                formData.append('File', file);
                formData.append('pos', pos);
                try {
                    await fetch('http://localhost:5000/upload', {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('3tography-access-token')}`,
                        }
                    });
                    await refresh();
                } catch (error) {
                    console.error(error);
                }
            }
            changeFile(null);
        }
        submit();
    }, [file]);

    const uploadImage = () => {
        input.current.click();
    }

    return (
        <>
            <div class='image-wrapper' onClick={uploadImage}>
                <img alt={url} src={url}></img>
            </div>
            <form>
                <input ref={input} onChange={handleInputChange} type='file' name='File' hidden/>
            </form>
        </>
    )
}

export default Image;