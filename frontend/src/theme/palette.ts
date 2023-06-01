import { PaletteMode } from '@mui/material';

export const light = {
    mode: 'light' as PaletteMode,
    primary: {
        main: 'rgb(0, 0, 0)',
        contrastText: 'rgb(255, 255, 255)',
    },
    text: {
        primary: 'rgb(40, 40, 40)',
        secondary: 'rgb(103, 119, 136)',
    },
    background: {
        paper: 'rgb(242, 243, 245)',
        default: 'rgb(255, 255, 255)',
    },
    divider: 'rgba(0, 0, 0, 0.12)',
};

export const dark = {
    mode: 'dark' as PaletteMode,
    primary: {
        main: 'rgb(255, 255, 255)',
        contrastText: 'rgb(0, 0, 0)',
    },
    text: {
        primary: 'rgb(255, 255, 255)',
        secondary: 'rgb(207, 207, 207)',
    },
    background: {
        default: 'rgb(0, 0, 0)',
        paper: 'rgb(15, 15, 15)',
    },
    divider: 'rgba(145, 158, 171, 0.24)',
};