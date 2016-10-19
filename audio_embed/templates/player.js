generateHtml = function(container) {
	var containerID = container.attr('id');	
	var preload = container.attr("preload") == "none" ? false : true;
	var srcAttr = 'url';
	if(preload) srcAttr = "src";

	//specify containercount to parent
	var nbContainer = container.parent().attr("containers");
	if(nbContainer) {
		nbContainer = parseInt(nbContainer)+1;
		container.parent().attr("containers", nbContainer);
	} else {
		container.parent().attr("containers", 1);
	}
	//insert main control
	container.prepend('<div class="main-control"><ul class="control"><li class="play"><a href="javascript://">play</a></li> <li class="pause"><a href="javascript://">pause</a></li> <li class="stop"><a href="javascript://">stop</a></li> <li class="repeat"><a href="javascript://">repeat</a></li></ul><div class="timebar-wrapper"><div class="timebar"></div></div></div>');
	var audioTags = container.find("audio");
	audioTags.detach();
	
	//insert tracks
	container.append('<ul class="tracks"></ul>');
	var containerTracks = container.find('.tracks');
	audioTags.each(function(i){
		containerTracks.append('<li class="track"><ul class="control"><li class="mute"><a href="javascript://">mute</a></li><li class="solo"><a href="javascript://"><span></span></a></li></ul><span class="status"></span><audio index="'+i+'" container="'+containerID+'"><source src ="'+$(this).attr("url") + '"/>Your browser does not support the audio element.</audio><span class="track-name">'+$(this).attr("name")+'</span>'+'</li>');
	});	
	container.append('<span class="loader"></span>');
	if(!preload) {
		container.append('<a class="loading-link" href="javascript://"></a>').addClass("waiting");
	}
	audioTags.remove();
};

initPlayer = function(containerID) {
	var container = $("#"+containerID);	
	generateHtml(container);
	
	//fast access to main control buttons and timebar
	NAME_player[containerID] = {
		tracks :  Array(), 
	 	playButton : container.find(".main-control .play"),
		pauseButton : container.find(".main-control .pause"),
		stopButton : container.find(".main-control .stop"),
		repeatButton : container.find(".main-control .repeat"),
		timebar : container.find(".main-control .timebar"),
		timebarWrapper : container.find(".main-control .timebar-wrapper"),
		firstTrack : null, 
		loadedAudio:0,
		playing:false, 
		repeat : false
	};
	NAME_player[containerID].playButton.attr('container', containerID);
	NAME_player[containerID].pauseButton.attr('container', containerID);
	NAME_player[containerID].stopButton.attr('container', containerID);
	NAME_player[containerID].repeatButton.attr('container', containerID);
	NAME_player[containerID].timebar.attr('container', containerID);
	NAME_player[containerID].timebarWrapper.attr('container', containerID);

	container.find(".tracks audio").each(function(i, value){
		var that = $(this);
		that.attr('container', containerID);
		NAME_player[containerID].tracks.push(that[0]);
		//load track
		that[0].load();
		that[0].addEventListener("canplaythrough", function() {
			NAME_player[containerID].loadedAudio++;
			if(NAME_player[containerID].loadedAudio==NAME_player[containerID].tracks.length) container.trigger("ready");
		}, false);
		that[0].addEventListener("error", function() {
			container.trigger("error", i+1);
		}, false);
		that.attr("index", i);
	});
	NAME_player[containerID].trackCount=NAME_player[containerID].tracks.length;
	NAME_player[containerID].firstTrack = NAME_player[containerID].tracks[0];
	container.on("ready", function(){
		$(this).addClass("ready");
	});
	container.on("error", function(e,i){
		$(this).addClass("error");
		$(this).find('.track:nth-child('+i+')').addClass("error");
	});
	
	//MUTE not active
	//----------------------------------------------
	container.on('click', '.tracks .track:not(.locked):not(.solo) .mute:not(.active) > a', function() {
		//switch button aspect
		var dad = $(this).parent();
		dad.addClass("active");
		dad.closest(".track").addClass("mute");
		
		//get track
		var track = $(this).closest('.track').find('audio:first')[0];
		
		//add volume to the track
		track.volume=0;
	});
	
	//MUTE active
	//----------------------------------------------
	container.on('click', '.tracks .track:not(.locked):not(.solo) .mute.active > a', function() {
		//switch button aspect
		var dad = $(this).parent();
		dad.removeClass("active");
		dad.closest(".track").removeClass("mute");
		
		//get track
		var track = $(this).closest('.track').find('audio:first')[0];
		
		//mute the track
		track.volume=1;
	});
	

	//SOLO not active
	//----------------------------------------------
	container.on('click', '.tracks .solo:not(.active) > a', function() {
		//switch button aspect
		var dad = $(this).parent();
		
		//mute all others
		dad.closest('.tracks').find(".track").removeClass("solo").addClass("locked").each(function() {
			//remove potential active solo track
			$(this).find(".solo.active").removeClass("active");

			//get track
			var track = $(this).find('audio:first')[0];
			track.volume=0;
		});

		dad.addClass("active");
		
		//remove locked class to my track and get audio track
		var track = dad.closest(".track").addClass("solo").removeClass("locked").find('audio:first')[0];
		
		//add volume to the track
		track.volume=1;

	});
	
	//SOLO active
	//----------------------------------------------
	container.on('click', '.tracks .solo.active > a', function() {
		//switch button aspect
		var dad = $(this).parent();
		
		//mute all others
		dad.closest('.tracks').find(".track").removeClass("locked solo").each(function() {
			//remove potential active solo track
			$(this).find(".solo.active").removeClass("active");

			//get track
			var track = $(this).find('audio:first')[0];
			if($(this).hasClass("mute"))
				track.volume=0;
			else
				track.volume=1;
		});
		dad.removeClass("active");
	});

	//PLAY
	//----------------------------------------------
	container.on('click', '.main-control .play:not(.active)', function() {
		var containerID = $(this).attr('container');
		NAME_player[containerID].pauseButton.removeClass("active");
		NAME_player[containerID].playButton.addClass("active");
		$.each(NAME_player[containerID].tracks, function(){
			this.play();
		});
		NAME_player[containerID].playing=true;
	});
	
	//LOAD
	//----------------------------------------------
	container.on('click', '.loading-link', function() {
		var container = $(this).closest(".audio-container");
		container.removeClass("waiting").find('audio').each(function(){
			$(this).attr("src", $(this).attr("url"));
		});
	});
	//REPEAT
	//----------------------------------------------
	container.on('click', '.main-control .repeat', function() {
		var containerID = $(this).attr('container');
		$(this).toggleClass("active");
		NAME_player[containerID].repeat = $(this).hasClass("active");
	});

	//PAUSE
	//----------------------------------------------
	container.on('click', '.main-control .play.active + .pause:not(.active)', function() {
		var containerID = $(this).attr('container');	
		NAME_player[containerID].playButton.removeClass("active");
		NAME_player[containerID].pauseButton.addClass("active");
		$.each(NAME_player[containerID].tracks, function(){
			this.pause();
		});
		NAME_player[containerID].playing=false;
	});
	
	//STOP
	//----------------------------------------------
	container.on('click', '.main-control .stop', function() {
		var containerID = $(this).attr('container');
		NAME_player[containerID].playButton.removeClass("active");
		NAME_player[containerID].pauseButton.removeClass("active");
		$.each(NAME_player[containerID].tracks, function(){
			this.pause();
			this.currentTime=0;
		});
		NAME_player[containerID].playing=false;
	});
	
	//SEEK BAR
	//----------------------------------------------
	container.on('click', '.main-control .timebar-wrapper', function(e) {
		var containerID = $(this).attr('container');
		//to be more sure : pause current playing
		NAME_player[containerID].tracks[0].pause();
		var myWidth = e.pageX - NAME_player[containerID].timebar.offset().left;
		var widthPercent = (myWidth*100)/NAME_player[containerID].timebarWrapper.width();
		timePercent = NAME_player[containerID].firstTrack.duration*widthPercent/100;
		
		//change the bar progression
		NAME_player[containerID].timebar.css('width', widthPercent+'%');
		
		//apply the wanted currentTime to all tracks
		//console.log((NAME_player[containerID].playing ? "playing":"not playing")+ ' currentTime='+timePercent+' => '+widthPercent+"%");
		
		for(var i=1;i<NAME_player[containerID].tracks.length;i++) {
			var trackI = NAME_player[containerID].tracks[i];
			trackI.currentTime=timePercent;
			//console.log('track['+i+'].currentTime='+trackI.currentTime+" != "+timePercent+' ????');
		
		}
		//apply the wanted current time to the first track (the observed one)
		NAME_player[containerID].tracks[0].currentTime=timePercent;	

		//play again if we were playing
		if(NAME_player[containerID].playing==true) NAME_player[containerID].tracks[0].play();
	});
	
	//TIME UPDATE
	//----------------------------------------------
	$(NAME_player[containerID].tracks[0]).bind('timeupdate', function() {
		var containerID = $(this).attr('container');
		
		//console.log("TIME UPDATE : "+NAME_player[containerID].firstTrack.currentTime);
		//change the bar progression
		NAME_player[containerID].timebar.css('width', ((NAME_player[containerID].firstTrack.currentTime*100) / NAME_player[containerID].firstTrack.duration)+'%');
	});

	$(NAME_player[containerID].tracks[0]).bind('ended', function() {
		//stop player if we terminate the track
		var containerID = $(this).attr('container');	
		NAME_player[containerID].stopButton.click();
		if(NAME_player[containerID].repeat)
			NAME_player[containerID].playButton.click();
	});
};

NAME_player = {};
initPlayer('NAME');
