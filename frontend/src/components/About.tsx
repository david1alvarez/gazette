import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useTheme } from '@mui/material/styles';

const About = (): JSX.Element => {
    const theme = useTheme();

    return (
        <div id='about'>
            <Box
                sx={{
                    pt: 5,
                    pb: 12,
                    px: 2,
                    backgroundColor: theme.palette.background.default,
                }}
            >
                <Box marginBottom={4}>
                    <Typography
                        variant='h5'
                        align='center'
                        color={theme.palette.text.primary}
                        fontWeight={700}
                        marginTop={theme.spacing(1)}
                        gutterBottom
                        sx={{
                            textTransform: 'uppercase',
                            mb: 2,
                        }}
                    >
                        About
                    </Typography>
                    <Typography
                        variant='subtitle1'
                        align='center'
                        color={theme.palette.text.secondary}
                        marginTop={theme.spacing(1)}
                        gutterBottom
                    >
                        Bringing the news of hostcity to you!
                    </Typography>
                </Box>
            </Box>
        </div>
    );
};

export default About;