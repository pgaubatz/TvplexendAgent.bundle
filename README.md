TvplexendAgent.bundle
=======================

This is a **metadata agent plugin** for the [Plex Media Server](https://plex.tv).
It provides metadata for [Tvheadend](https://tvheadend.org) recordings to the Plex Media Server.

Instructions
------------

1. Follow the Plex' [instructions](https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-) on *how to manually install a [plugin]* (please ignore the word *channel*, installing an agent is no different than installing a channel!).
2. Open the Plex' Web Interface (e.g., [http://plex.local:32400/web/index.html](http://plex.local:32400/web/index.html)) and find the following settings dialog: <br>![agent settings screenshot](https://raw.githubusercontent.com/pgaubatz/TvplexendAgent.bundle/master/TvplexendAgent-Screenshot-1.png)
3. Configure the Tvheadend agent by clicking the ![settings](http://cdn-img.easyicon.net/png/10734/1073494.png) icon. Note that you *must* specify the URL (e.g., _http://localhost:9981/_) of the Tvheadend Web-Interface!
4. Edit the library that contains your Tvheadend recordings by clicking the ![pencil](http://cdn-img.easyicon.net/png/10691/1069172.png) icon: <br>![library settings screenshot](https://raw.githubusercontent.com/pgaubatz/TvplexendAgent.bundle/master/TvplexendAgent-Screenshot-2.png)
5. Select the **Tvplexend** agent and click *save changes*: <br>![edit library settings screenshot](https://raw.githubusercontent.com/pgaubatz/TvplexendAgent.bundle/master/TvplexendAgent-Screenshot-3.png)
6. Enjoy metadata for your Tvheadend recordings!

Troubleshooting
---------------

- If something goes wrong, make sure that Tvheadend's HTTP-API can be reached. You can easily check this by opening, e.g., _http://localhost:9981/api/serverinfo_ in your favorite Web browser. If Tvheadend is configured correctly, it should immediately return a JSON document (e.g, `{"sw_version": "3.9...`).

See Also
--------

You might also want to check out the corresponding **channel plugin**: [TvplexendChannel.bundle](https://github.com/pgaubatz/TvplexendChannel.bundle).
