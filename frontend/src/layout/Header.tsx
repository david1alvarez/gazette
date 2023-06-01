import React, { useContext } from 'react';
import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Link from '@mui/material/Link';
import Toolbar from '@mui/material/Toolbar';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import NotificationsIcon from '@mui/icons-material/Notifications';
import MenuIcon from '@mui/icons-material/Menu';
import { alpha, useTheme } from '@mui/material/styles';

import ColorModeContext from '../utils/ColorModeContext';

const Header = (): JSX.Element => {
    const theme = useTheme();
    const colorMode = useContext(ColorModeContext);

    return (
        <>
            <AppBar
                color='transparent'
                position='sticky'
                sx={{
                    border: 0,
                    padding: '10px 0',
                    marginBottom: '5px',
                    top: 'auto',
                    boxShadow: '0 4px 18px 0px rgba(0, 0, 0, 0.12), 0 7px 10px -5px rgba(0, 0, 0, 0.15)'
                }}
            >
                <Toolbar sx={{ minHeight: 70 }}>
                    <Link href='/' sx={{ textDecoration: 'none' }}>
                        <IconButton size='large' disabled>
                            <NotificationsIcon
                                sx={{
                                    color: theme.palette.primary.main,
                                    height: 40,
                                    width: 40
                                }}
                            />
                            <Box sx={{ display: { md: 'inline', xs: 'none' } }}>
                                <Typography
                                    variant='h6'
                                    sx={{
                                        flexGrow: 1,
                                        color: theme.palette.text.primary,
                                        fontWeight: 'bold',
                                        textTransform: 'uppercase',
                                        textDecoration: 'none',
                                        marginLeft: '10px'
                                    }}
                                >
                                    Gazette
                                </Typography>
                            </Box>
                        </IconButton>
                    </Link>
                    <Box sx={{ flexGrow: 1 }} />
                    <Box
                        sx={{
                            alignItems: 'center',
                            display: { lg: 'flex', md: 'none', xs: 'none' }
                        }}
                    >
                        <Button
                            component='a'
                            color='primary'
                            href='#about'
                            variant='text'
                            sx={{
                                color: theme.palette.text.primary,
                                textTransform: 'uppercase',
                                mx: 1.5,
                                marginLeft: '15px',
                                '&:active': {
                                    color: theme.palette.primary.main,
                                },
                                '&:hover': {
                                    color: theme.palette.primary.main,
                                },
                            }}
                        >
                            About
                        </Button>
                    </Box>
                    <Divider
                        orientation='vertical'
                        sx={{
                            height: 32,
                            mx: 2,
                            display: { lg: 'flex', md: 'none', xs: 'none' }
                        }}
                    />
                    <Box sx={{ display: 'flex' }}>
                        <IconButton
                            onClick={colorMode.toggleColorMode}
                            aria-label='Theme Mode'
                            color={theme.palette.mode === 'dark' ? 'warning' : 'inherit'}
                        >
                            {theme.palette.mode === 'dark'
                                ? (
                                    <Tooltip title='Turn on the light'>
                                        <LightModeIcon fontSize='medium' />
                                    </Tooltip>
                                )
                                : (
                                    <Tooltip title='Turn off the light'>
                                        <DarkModeIcon fontSize='medium' />
                                    </Tooltip>
                                )
                            }
                        </IconButton>
                    </Box>
                    <Box
                        sx={{
                            display: { md: 'block', lg: 'none' }
                        }}
                        alignItems='center'
                    >
                        <Button
                            onClick={() => { }}
                            aria-label='Menu'
                            variant='outlined'
                            sx={{
                                borderRadius: 0,
                                minWidth: 'auto',
                                padding: 1,
                                borderColor: alpha(theme.palette.divider, 0.2)
                            }}
                        >
                            <MenuIcon
                                sx={{
                                    color: theme.palette.primary.main
                                }}
                            />
                        </Button>
                    </Box>
                </Toolbar>
            </AppBar>
        </>
    );
};

export default Header;