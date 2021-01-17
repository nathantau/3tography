const host = process.env.REACT_APP_FLASK_HOST;

const FeedUtils = {
    getFollowing: async () => {
        /**
         * Returns a list of user objects in the form:
         * {
         *  user: 'username',
         *  imageUrls: []
         * }
         */
        try {
            let res = await fetch(`${host}/api/following`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('3tography-access-token')}` }
            });
            res = await res.json();
            return res.following;
        } catch (err) {
            console.error(err);
        }
        return [];
    }
}

export default FeedUtils;
