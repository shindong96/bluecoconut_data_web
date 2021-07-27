//------------------------------------------------------------------------------------------------------------------------------------------------------------

var map;
var infowindow;
var clickedMarker;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 3,
    center: new google.maps.LatLng(37.549012, 126.988546),
    mapTypeId: "satellite",
  });

  infowindow = new google.maps.InfoWindow();
  for (var i = 0; i < argos.length; i++) {
    marker = new google.maps.Marker({
      title: argos[i].number,
      position: new google.maps.LatLng(argos[i].lat, argos[i].lng),
      map: map,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 6,
        fillOpacity: 1.0,
        fillColor: "#FFFF00",
        strokeWeight: 1,
      },
    });

    // const contentString =
    //   "<div>" +
    //   `<a href="#" onclick="showCycle(${argos[i].number})">` +
    //   // `<a class="cycle" name="${argos[i].number}">` +
    //   // `<a id="${argos[i].number}" href="#">` +
    //   "ArgoNumber: " +
    //   argos[i].number +
    //   "</a>" +
    //   "<BR>" +
    //   "위도: " +
    //   argos[i].lat +
    //   "<BR>" +
    //   "경도: " +
    //   argos[i].lng +
    //   "</div>";

    const contentString = `<div class="argo-marker-content">
    <div class="argo-marker-content__title">
        <div>
            <div>
              <span class="argo-number">ArogoNumber: ${argos[i].number}</span>
            </div>
            <i class="fas fa-table fa-lg" onclick="moveArgoTable(${argos[i].number})"></i>
        </div>
        <div>
            <i class="fas fa-file-download fa-lg" onclick="downloadArgoData(${argos[i].number})"></i>
        </div>
    </div>
    <div class="argo-marker-content__cycle">
        <div>
            <span onclick="showCycle(${argos[i].number})">Show trajectory</span>
        </div>
    </div>
    <div class="argo-marker-content__summary">
        <div>
            <div>
                <span class="argo-subtext">Launched</span>
            </div>
            <div>
                <span class="argo-text">${argos[i].source_time}</span>
            </div>
            <div>
                <span class="argo-subtext">Last Cycle</span>
            </div>
            <div>
                <span class="argo-text">${argos[i].cycle}</span>
            </div>
        </div>
        <div>
            <div>
                <span class="argo-subtext">Visualization</span>
            </div>
            <div>
                <i class="fas fa-chart-bar fa-lg" onclick="visualizeArgoData(${argos[i].number})"></i>
            </div>
            <div>
                <span class="argo-subtext">Last Tx</span>
            </div>
            <div>
                <span class="argo-text">${argos[i].last_time}</span>
            </div>
        </div>
    </div>
</div>`;

    google.maps.event.addListener(
      marker,
      "click",
      (function (marker, i) {
        return function () {
          infowindow.setContent(contentString);
          infowindow.open(map, marker);
          if (clickedMarker) {
            clickedMarker.setIcon({
              path: google.maps.SymbolPath.CIRCLE,
              scale: 6,
              fillOpacity: 1.0,
              fillColor: "#FFFF00",
              strokeWeight: 1,
            });
          }
          clickedMarker = marker;
          clickedMarker.setIcon({
            path: google.maps.SymbolPath.CIRCLE,
            scale: 8,
            fillOpacity: 1.0,
            fillColor: "#FF0000",
            strokeWeight: 3,
          });
        };
      })(marker, i)
    );

    if (marker) {
      marker.addListener("click", function () {
        // 줌(zoom) 기능 뺌
        // map.setZoom(8);
        // map.setCenter(this.getPosition());
      });
    }

    // google.maps.event.addListener(
    //   marker,
    //   "click",
    //   (function (marker, i) {
    //     return function () {
    //       infowindow.setContent("추후 사이클 보여주는 기능구현");
    //       infowindow.open(map, marker);
    //     };
    //   })(marker, i)
    // );
  }
}

//------------------------------------------------------------------------------------------------------------------------------------------------------------

// 구본이가 만들어줄 부분2
function moveArgoTable(argo_number) {
  getPk = argo_number;
  if (confirm(getPk + '번 Argo 테이블 조회하시겠습니까?')) {
    window.location.href = '/table_view/detail/' + getPk;
    console.log(`move argo table: ${argo_number}`);
  } else {
  }
}

function downloadArgoData(argo_number) {
  getPk = argo_number;
  if (confirm(getPk + '번 Argo 관측정보를 다운로드 하시겠습니까?')) {
    $.ajax({
      url: "/table_view/download/" + getPk,
      type: "GET",
      dataType: "json",
      data: {
          'csrfmiddlewaretoken': '{{ csrf_token }}',
          pk: getPk,
      },
      success: function(data) {
          alert(data.message);
          download_url = '../../static/csv_file/download.csv'
          window.location.assign(download_url);
          console.log("SUCCESS!")
      },
      error: function(data) {
        download_url = '../../static/csv_file/download.csv'
        window.location.assign(download_url);
        console.log("SUCCESS!")
      },
    });
  } else {
  }
}

function visualizeArgoData(argo_number) {
  $("#modal-argo").modal('show');
  console.log(`visualize argo data: ${argo_number}`);
}

// 구현 순서
// 1.polyline으로 사이클 선 추가
// addCycleLine()
// 현재 기존의 map 객체를 가져와서 추가하는 부분을 못함

// 2.다른 디자인의 사이클 마커 추가
// addCycleMarker()

// 3.사이클 마커에 setContent(->table data)

// 4.디자인 보완
//  - 마커
//  - 사이클 마커, 사이클 선 디자인
var polyArr = [];
var markerArr = [];
var myInterval;

function showCycle(argo_number) {
  $.ajax({
    url: `argo_data/${argo_number}`,
    type: "GET",
    dataType: "json",
    data: {
      pk: argo_number,
      csrfmiddlewaretoken: "{{ csrf_token }}",
    },
    success: function (data) {
      // console.log(data);
      clearInterval(myInterval);
      deletePoly();
      deleteMarker();
      addCycleMarker(data, argo_number);
      addCycleLine(data);
    },
    error: function (error) {
      console.log("this is error");
      console.log(error);
    },
  });
}

function deletePoly() {
  var size = polyArr.length;
  for (var i = 0; i < size; i++) {
    var t = polyArr.pop();
    t.setOptions({
      strokeColor: "#808080",
    });
  }
}

function deleteMarker() {
  var size = markerArr.length;
  for (var i = 0; i < size; i++) {
    var t = markerArr.pop();
    var p = new google.maps.Point(
      t.getIcon()["labelOrigin"]["x"],
      t.getIcon()["labelOrigin"]["y"]
    );
    t.setIcon({
      path: google.maps.SymbolPath.CIRCLE,
      scale: 4,
      fillOpacity: 1.0,
      fillColor: "#808080",
      strokeOpacity: 0,
      labelOrigin: p,
    });
  }
}

function addCycleLine(data) {
  // console.log(data);
  // console.log(data["argoCycleDatas"]);
  const cycleCoordinates = data["argoCycleDatas"];

  // i = 0;
  // let timerId = null;
  // setInterval(addOneLine, 1000);
  function addOneLine(i) {
    let twoPointForLine = [
      { lat: cycleCoordinates[i].lat, lng: cycleCoordinates[i].lng },
      { lat: cycleCoordinates[i + 1].lat, lng: cycleCoordinates[i + 1].lng },
    ];
    let cyclePath = new google.maps.Polyline({
      path: twoPointForLine,
      geodesic: true,
      strokeColor: "#FF0000",
      strokeOpacity: 1.0,
      strokeWeight: 2,
      geodesic: true, //set to false if you want straight line instead of arc
    });
    polyArr.push(cyclePath);
    cyclePath.setMap(map);
    // if (i == cycleCoordinates.length - 1) {
    //   clearInterval(timerId);
    // }
  }

  var i = 0;
  if (cycleCoordinates.length >= 2) {
    myInterval = setInterval(function () {
      if (i == cycleCoordinates.length - 2) clearInterval(myInterval);
      addOneLine(i);
      i++;
    }, 100);
  }

  /*const timer = ms =>new Promise(res=>setTimeout(res,ms))

  async function load(){
    for(var i = 0 ; i < cycleCoordinates.length - 1; i++){
      addOneLine(i);
      await timer(100);
    }
  }
  load();*/

  // for (i = 0; i < cycleCoordinates.length - 1; i++) {
  //   let twoPointForLine = [
  //     { lat: cycleCoordinates[i].lat, lng: cycleCoordinates[i].lng },
  //     { lat: cycleCoordinates[i + 1].lat, lng: cycleCoordinates[i + 1].lng },
  //   ];
  //   const cyclePath = new google.maps.Polyline({
  //     path: twoPointForLine,
  //     geodesic: true,
  //     strokeColor: "#FF0000",
  //     strokeOpacity: 1.0,
  //     strokeWeight: 2,
  //     geodesic: true, //set to false if you want straight line instead of arc
  //   });
  //   cyclePath.setMap(map);
  // }
}

//   const cyclePath = new google.maps.Polyline({
//     path: cycleCoordinates,
//     geodesic: true,
//     strokeColor: "#FF0000",
//     strokeOpacity: 1.0,
//     strokeWeight: 2,
//     geodesic: true, //set to false if you want straight line instead of arc
//   });
//   cyclePath.setMap(map);
// }

function addCycleMarker(data, argo_number) {
  const argoCycleDatas = data["argoCycleDatas"];
  // console.log(argoCycleDatas);
  infowindow = new google.maps.InfoWindow();
  // labelPointXY = {X: a, Y: b}
  let labelPointXY;
  for (i = 0; i < argoCycleDatas.length; i++) {
    if (i != argoCycleDatas.length - 1) {
      labelPointXY = calCycleLablePosition(
        argoCycleDatas[i].lng,
        argoCycleDatas[i].lat,
        argoCycleDatas[i + 1].lng,
        argoCycleDatas[i + 1].lat
      );
    } else {
      // 다음 사이클이 없는 마지막의 경우에는 마지막전의 label방향과 같은 방향으로 설정
    }

    if (i == argoCycleDatas.length / 2) {
      function center() {
        map.setCenter(
          new google.maps.LatLng(argoCycleDatas[i].lat, argoCycleDatas[i].lng)
        );
        map.setZoom(8);
      }
      center(); //사이클 중앙으로 zoom
    }

    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(
        argoCycleDatas[i].lat,
        argoCycleDatas[i].lng
      ),
      map: map,
      label: {
        text: `${argoCycleDatas[i].cycle_number}`,
        color: "#FFFFFF",
        fontSize: "12px",
      },
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 4,
        fillOpacity: 1.0,
        fillColor: "#FF0000",
        strokeOpacity: 0,
        labelOrigin: new google.maps.Point(
          labelPointXY["X"],
          labelPointXY["Y"]
        ),
      },
    });
    markerArr.push(marker);

    const contentString = `
    <div class="cycle-marker-content">
    <div class="argo-marker-content__title">
        <div>
            <span class="argo-number">${argo_number} - Cycle ${argoCycleDatas[i].cycle_number}</span>
            <i class="fas fa-table fa-lg" onclick="moveCycleTable(${argo_number}, ${argoCycleDatas[i].cycle_number})"></i>
        </div>
        <div>
            <i class="fas fa-file-download fa-lg" onclick="downloadCycleData(${argo_number}, ${argoCycleDatas[i].cycle_number})"></i>
        </div>
    </div>
    <div class="argo-marker-content__summary">
        <div>
            <div>
                <span class="argo-subtext">Date</span>
            </div>
            <div>
                <span class="argo-text">${argoCycleDatas[i].time}</span>
            </div>
            <div>
                <span class="argo-subtext">Latitude</span>
            </div>
            <div>
                <span class="argo-text">${argoCycleDatas[i].lat}</span>
            </div>
        </div>
        <div>
            <div>
                <span class="argo-subtext">Visualization</span>
            </div>
            <div>
                <i class="fas fa-chart-bar fa-lg" onclick="visualizeCycleData(${argo_number}, ${argoCycleDatas[i].cycle_number})"></i>
            </div>
            <div>
                <span class="argo-subtext">Longitude</span>
            </div>
            <div>
                <span class="argo-text">${argoCycleDatas[i].lng}</span>
            </div>
        </div>
    </div>
</div>`;

    // const contentString =
    //   "<div>" +
    //   `<a href="#">` +
    //   `${argo_number}` +
    //   "</a>" +
    //   " - Cycle " +
    //   argoCycleDatas[i].cycle_number +
    //   "<BR>" +
    //   "위도: " +
    //   argoCycleDatas[i].lat +
    //   "<BR>" +
    //   "경도: " +
    //   argoCycleDatas[i].lng +
    //   "</div>";

    google.maps.event.addListener(
      marker,
      "click",
      (function (marker, i) {
        return function () {
          infowindow.setContent(contentString);
          infowindow.open(map, marker);
        };
      })(marker, i)
    );
  }
}

// 구본이가 만들어줄 부분1
function moveCycleTable(argo_number, cycle_number) {
  console.log(`move cycle table: ${argo_number}-${cycle_number}`);
  getPk = argo_number;
  cycle = cycle_number;
  if (confirm(getPk + '번 Argo 해당 Cycle 테이블을 조회하시겠습니까?')) {
    window.location.href = '/table_view/detail/' + getPk +'?cycleSelect=' + cycle;
    console.log(`move argo table: ${argo_number}`);
  } else {
  }
}

function downloadCycleData(argo_number, cycle_number) {
  console.log(`download cycle data: ${argo_number}-${cycle_number}`);
  getPk = argo_number;
  cycle = cycle_number;
  if (confirm(getPk + '번 Argo 해당 Cycle 데이터를 다운로드 하시겠습니까?')) {
    $.ajax({
      url: "/table_view/cycle_download/" + getPk + "/" + cycle,
      type: "GET",
      dataType: "json",
      data: {
          'csrfmiddlewaretoken': '{{ csrf_token }}',
          pk: getPk,
          cycle: cycle,
      },
      success: function(data) {
          alert(data.message);
          download_url = '../../static/csv_file/download.csv'
          window.location.assign(download_url);
          console.log("SUCCESS!")
      },
      error: function(data) {
        download_url = '../../static/csv_file/download.csv'
        window.location.assign(download_url);
        console.log("SUCCESS!")
      },
    });
  } else {
  }
}

function visualizeCycleData(argo_number, cycle_number) {
  console.log(`visualize cycle data: ${argo_number}-${cycle_number}`);
  $("#modal-cycle").modal('show');
  // $.ajax({
  //   url: "/map/csv_update/" + argo_number + "/" + cycle_number,
  //   type: "GET",
  //   dataType: "text",
  //   data: {
  //       'csrfmiddlewaretoken': '{{ csrf_token }}',
  //       pk: argo_number,
  //       cycle: cycle_number,
  //   },
  //   success: function(data) {
  //     $("#modal-cycle").modal('show');
  //       console.log("SUCCESS!")
  //   },
  //   error: function(data) {
  //     $("#modal-cycle").modal('show');
  //     console.log("Fail!")
  //   },
  // });
}

function calCycleLablePosition(x1, y1, x2, y2) {
  // google.maps.Point는 좌표평면과 y의 +/-가 반대로 정의되어 있음
  // delta벡터와 직교(반시계 방향으로 +90도)하게 Position 부여
  const DISTANCE = 3;
  let a = 0;
  let b = 0;
  const deltaX = x2 - x1;
  const deltaY = y2 - y1;
  const m = deltaY / deltaX;
  // 1.delta벡터가 좌표평면 양의 x축
  if (m >= -1 / 2 && m < 1 / 2 && deltaX >= 0) {
    a = 0;
    b = -1;
    // 2.delta벡터가 좌표평면 1사분면
  } else if (m >= 1 / 2 && m < 3 / 2 && deltaX >= 0 && deltaY >= 0) {
    a = -1;
    b = -1;
    // 3.delta벡터가 좌표평면 양의 y축
  } else if (
    (m < -3 / 2 && deltaX < 0 && deltaY >= 0) ||
    (m >= 3 / 2 && deltaX >= 0 && deltaY >= 0)
  ) {
    a = -1;
    b = 0;
    // 4.delta벡터가 좌표평면 2사분면
  } else if (m >= -3 / 2 && m < -1 / 2 && deltaX < 0 && deltaY >= 0) {
    a = -1;
    b = 1;
    // 5.delta벡터가 좌표평면 음의 x축
  } else if (m >= -1 / 2 && m < 1 / 2 && deltaX < 0) {
    a = 0;
    b = 1;
    // 6.delta벡터가 좌표평면 3사분면
  } else if (m >= 1 / 2 && m < 3 / 2 && deltaX < 0 && deltaY < 0) {
    a = 1;
    b = 1;
    // 7.delta벡터가 좌표평면 음의 y축
  } else if (
    (m < -3 / 2 && deltaX >= 0 && deltaY < 0) ||
    (m >= 3 / 2 && deltaX < 0 && deltaY < 0)
  ) {
    a = 1;
    b = 0;
    // 8.delta벡터가 좌표평면 4사분면
  } else if (m >= -3 / 2 && m < -1 / 2 && deltaX >= 0 && deltaY < 0) {
    a = 1;
    b = -1;
  }
  return { X: a * DISTANCE, Y: b * DISTANCE };
}
