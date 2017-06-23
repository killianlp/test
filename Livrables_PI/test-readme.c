/* Ce fichier est a placer dans gst-rtsp-server/examples
 * Dans l'appel de la fonction gst_rtsp_media_factory_set_launch (),
 * Il faut décommenter les arguments selon ce que l'on veut faire 
 */

/* GStreamer
 * Copyright (C) 2008 Wim Taymans <wim.taymans at gmail.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
 * Boston, MA 02110-1301, USA.
 */

#include <gst/gst.h>
#include <gst/rtsp-server/rtsp-server.h>

int main (int argc, char *argv[]) {
	GMainLoop *loop;
	GstRTSPServer *server;
	GstRTSPMountPoints *mounts;
	GstRTSPMediaFactory *factory;
	
	gst_init (&argc, &argv);
	
	loop = g_main_loop_new (NULL, FALSE);
	
	/* create a server instance */
	server = gst_rtsp_server_new ();
	
	/* get the mount points for this server, every server has a default object
	* that be used to map uri mount points to media factories */
	mounts = gst_rtsp_server_get_mount_points (server);
	
	/* make a media factory for a test stream. The default media factory can use
	* gst-launch syntax to create pipelines. 
	* any launch line works as long as it contains elements named pay%d. Each
	* element with pay%d names will be a stream */
	factory = gst_rtsp_media_factory_new ();
	gst_rtsp_media_factory_set_launch (factory,
	
	/*mire avec encodage logiciel*/
	//	"( videotestsrc ! video/x-raw, width=1920, height=1080, framerate=25/1 ! x264enc bitrate=5400 ! video/x-h264 ! rtph264pay name=pay0 pt=96 config-interval=2 )");
	
	/*mire avec encodage materiel*/
		"( videotestsrc ! video/x-raw, width=1920, height=1080, framerate=25/1 ! omxh264enc ! video/x-h264, profile=high ! rtph264pay name=pay0 pt=96 config-interval=2 )");
		
	/*flux video webcam avec encodage materiel*/
	//	"( v4l2src device=/dev/video0 ! videoconvert ! video/x-raw ! omxh264enc tune=zerolatency ! video/x-h264, profile=high ! rtph264pay name=pay0 pt=96 config-interval=2 )");
	
	/*flux video pour la diffusion d’un écran par le port CSI-2*/
	// "( v4l2src device=/dev/video0 ! videoconvert ! omxh264enc ! video/x-h264, profile=high, width=1920, height=1080, framerate=25/1! rtph264pay name=pay0 pt=96 config-interval=2 )");

	gst_rtsp_media_factory_set_shared (factory, TRUE);
	
	/* attach the test factory to the /test url */
	gst_rtsp_mount_points_add_factory (mounts, "/test", factory);
	
	/* don't need the ref to the mapper anymore */
	g_object_unref (mounts);
	
	/* attach the server to the default maincontext */
	gst_rtsp_server_attach (server, NULL);
	
	/* start serving */
	g_print ("stream ready at rtsp://127.0.0.1:8554/test\n");
	g_main_loop_run (loop);
	
	return 0;
}
