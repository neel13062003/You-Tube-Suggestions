const { google } = require("googleapis");


// Set up the YouTube API client
const youtube = google.youtube({
    version: "v3",
    auth: process.env.YOUTUBE_API,
});

module.exports = {

    getVideos: async (query) => {
        try {
            const { data } = await youtube.search.list({
                part: "id,snippet",
                q: query,
                type: "video",
                maxResults: 10,
            });

            let videos = data.items.map((item) => ({
                title: item.snippet.title,
                description: item.snippet.description,
                thumbnail: item.snippet.thumbnails.default.url,
                videoId: item.id.videoId,
            }));

            return videos;
        } catch (error) {
            console.error(error);
        }
    },

    getHomeVideos: async () => {
        try {
            const { data } = await youtube.search.list({
                chart: 'mostPopular',
                part: 'snippet',
                maxResults: 20
            });

            let videos = data.items.map((item) => ({
                title: item.snippet.title,
                description: item.snippet.description,
                thumbnail: item.snippet.thumbnails.default.url,
                videoId: item.id.videoId,
            }));

            return videos;
        } catch (error) {
            console.error(error);
        }
    },

}

