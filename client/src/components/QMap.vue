<template>
  <div id="map" class="q-map"></div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "QMap",
  emits: ["select"],
  setup(_, { emit }) {
    const init = function () {
      const myMap = new (window as any).ymaps.Map(
        "map",
        {
          center: [55.753, 37.622],
          zoom: 13,
          controls: [],
        },
        {
          yandexMapDisablePoiInteractivity: true,
        }
      );

      (window as any).ymaps
        .geocode(myMap.getCenter(), {
          kind: "metro",
          results: 50,
        })
        .then(function (res: any) {
          res.geoObjects.each((geoObject: any) => {
            if (geoObject.getPremise()) {
              geoObject.options.set("preset", "islands#redCircleIcon");
              myMap.geoObjects.add(geoObject);
              geoObject.events.add("click", function (event: any) {
                let geoObject = event.get("target");
                emit("select", {
                  name: geoObject.getPremise(),
                  coords: geoObject.geometry.getCoordinates(),
                });
              });
            }
          });
        });
    };

    (window as any).ymaps.ready(init);
  },
});
</script>

<style scoped lang="scss">
.q-map {
  width: 100%;
  height: 100%;
}
</style>
