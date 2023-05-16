import React from 'react'

export const NewSiteForm = () => {
    return (
        <form>
            <label for="url"></label>
            <input type="url" class="new-site-input" name="url" placeholder="example.com" required></input><br/>
            <h6 id="mobile-app-desc">"Mobile web apps" are websites that function in-browser in a very similar way to that of content downloaded from app stores</h6>

            <h4>Site Name:</h4>
            <input type="text" class="new-site-input" name="site-name" placeholder="Eventbrite" required></input><br/>

            <h4>Brief Description:</h4>
            <input type="text" id="brief_description" name="brief_description" required></input><br/>

            <label for="description_language">Description Language:</label>
            <select id="description_language" name="description_language">
                <option value="English">English</option>
                <option value="French">French</option>
                <option value="German">German</option>
                <option value="Spanish">Spanish</option>
            </select><br/>

            <h4>Keywords:</h4>
            <input type="text" id="keywords" name="keywords"></input><br/>

            <h4>Upload up to 4 Screenshots:</h4>
            <div className="upload-buttons">
                <label htmlFor="file-upload-1" className="upload-btn">
                UPLOAD
                <input type="file" id="file-upload-1" />
                </label>
                <label htmlFor="file-upload-2" className="upload-btn">
                UPLOAD
                <input type="file" id="file-upload-2" />
                </label>
                <label htmlFor="file-upload-3" className="upload-btn">
                UPLOAD
                <input type="file" id="file-upload-3" />
                </label>
                <label htmlFor="file-upload-4" className="upload-btn">
                UPLOAD
                <input type="file" id="file-upload-4" />
                </label>
            </div>

            <h5>If you own this app, please submit an email using the same domain as the url above. This will generate an email to create an admin account.</h5>
            <label for="admin_email">Admin Email:</label>
            <input type="email" id="admin_email" name="admin_email" placeholder="tech@example.com"></input><br/>

            <input type="submit" id="submit-site-btn" value="Submit"></input>
            </form>
    )
}