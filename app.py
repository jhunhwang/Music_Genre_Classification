import intro
import spotify_scraper_demo
import model_demo
from multiapp import MultiApp

app = MultiApp()
app.add_app("Brief Description of the Project", intro.app)
app.add_app("Spotify Song Features / Lyrics Scraper Demo", spotify_scraper_demo.app)
app.add_app("Western VS K-Pop Music Track Classifier", model_demo.app)
app.run()