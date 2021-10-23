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
          results: 30,
        })
        .then(function (res: any) {
          res.geoObjects.options.set("preset", "islands#redCircleIcon");
          res.geoObjects.events
            // При наведении на метку показываем хинт с названием станции метро.
            .add("click", function (event: any) {
              var geoObject = event.get("target");
              emit("select", {
                name: geoObject.getPremise(),
                coords: geoObject.geometry.getCoordinates(),
              });
              myMap.hint.open(
                geoObject.geometry.getCoordinates(),
                geoObject.getPremise()
              );
            })
            // Скрываем хинт при выходе курсора за пределы метки.
            .add("mouseleave", function (event: any) {
              myMap.hint.close(true);
            });
          // Добавляем коллекцию найденных геообъектов на карту.
          myMap.geoObjects.add(res.geoObjects);
          // Масштабируем карту на область видимости коллекции.
          myMap.setBounds(res.geoObjects.getBounds());
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
