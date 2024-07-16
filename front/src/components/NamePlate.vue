<template>
  <div class="name-container">
    <div class="prism">
      <div :class="['face', 'front', sizeClass]">
        <div class="text">{{ name }}</div>
      </div>
      <div class="face rear"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NamePlate',
  props: {
    name: String
  },
  computed: {
    sizeClass() {
      return `size-${this.name.length}`;
    }
  }
};
</script>

<style lang="scss" scoped>
@mixin set-font-size($size, $width, $height) {
  $characterWidth: 1.13125;

  $fontSize: 8px;
  @if ($size < calc($width / ($characterWidth * 16px))) {
    $fontSize: 16px;
  } @else if ($size < calc($width / ($characterWidth * 14px))) {
    $fontSize: 14px;
  } @else if (ceil(calc($size / 2)) < calc($width / ($characterWidth * 14px))) {
    $fontSize: 14px;
  } @else if (ceil(calc($size / 2)) < calc($width / ($characterWidth * 13px))) {
    $fontSize: 13px;
  } @else if (ceil(calc($size / 2)) < calc($width / ($characterWidth * 12px))) {
    $fontSize: 12px;
  } @else if (ceil(calc($size / 2)) < calc($width / ($characterWidth * 11px))) {
    $fontSize: 11px;
  } @else if (ceil(calc($size / 2)) < calc($width / ($characterWidth * 10px))) {
    $fontSize: 10px;
  } @else if (ceil(calc($size / 3)) < calc($width / ($characterWidth * 10px))) {
    $fontSize: 10px;
  } @else if (ceil(calc($size / 3)) < calc($width / ($characterWidth * 9.5px))) {
    $fontSize: 9.5px;
  } @else if (ceil(calc($size / 3)) < calc($width / ($characterWidth * 8.5px))) {
    $fontSize: 8.5px;
  }

  $lineCount: floor(calc($height / $fontSize));
  font-size: $fontSize;
  line-height: calc($height / $lineCount);
}

.name-container {
  perspective: 1000px;

  .prism {
    position: relative;
    width: 30px;
    transform-style: preserve-3d;
    transform: rotateX(-30deg) rotateY(15deg);
    height: 30px;

    .face {
      position: absolute;
      backface-visibility: hidden;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

      &.front {
        transform: translateZ(30px);
        height: 32px;
        width: 100px;
        padding: 2px 4px;
        background-color: #4f200f;
        border-top: solid 1px #666666;

        display: flex;
        flex-direction: column;
        justify-content: center;

        .text {
          color: #ffffff;
          font-family: 'Georgia', serif;
          font-weight: bold;
          max-height: 100%;
          max-width: 100%;
          overflow: hidden;
          word-break: break-all;
          text-align: center;
          text-transform: uppercase;
          text-shadow: 0.5px 0.5px #c76c3f;
        }

        // Iterate and apply the mixin for font-size based on size class
        @for $i from 1 through 32 {
          &.size-#{$i} {
            .text {
              @include set-font-size($i, 100px, 32px);
            }
          }
        }
      }

      &.rear {
        transform: rotateX(-45deg) translateX(1.5px);
        height: 32px;
        width: 32px;
        padding: 10px;
        background-color: #271810;
      }
    }
  }
}
</style>
