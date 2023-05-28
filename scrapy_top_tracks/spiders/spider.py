import scrapy


class TopTracksSpider(scrapy.Spider):
    
    name = "top_tracks"
    failure = False
    top_tracks_url = "https://pitchfork.com/reviews/best/tracks/"
    page = 0

    custom_settings = {
        "CLOSESPIDER_TIMEOUT": 30
    }

    def start_requests(self):
        while True:
            TopTracksSpider.page += 1
            yield scrapy.Request(url=f"{TopTracksSpider.top_tracks_url}?page={TopTracksSpider.page}", callback=self.parse)

    def parse(self, resp):

        tracks = []

        first_track_elem = resp.css("div.track-hero")
        if first_track_elem:
            tracks.append({
                "title": first_track_elem.css("h2.title::text").get(),
                "artists": first_track_elem.css("ul.artist-list li::text").getall(),
                "genres": first_track_elem.css("li.genre-list__item a::text").getall(),
                "link": first_track_elem.css("a.artwork::attr(href)").get(),
                "time_published": first_track_elem.css("time.pub-date::attr(datetime)").get(),
            })
        
        track_elems = resp.css("div.track-collection-item")
        for track in track_elems:
            tracks.append({
                "title": track.css("h2.track-collection-item__title::text").get(),
                "artists": track.css("ul.artist-list li::text").getall(),
                "genres": track.css("li.genre-list__item a::text").getall(),
                "link": track.css("a.track-collection-item__track-link::attr(href)").get(),
                "time_published": track.css("time.pub-date::attr(datetime)").get()
            })

        for track in tracks:
            yield track
