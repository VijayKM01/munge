/*****************************************************************************
 *  $Id: cred.c,v 1.1 2003/04/08 18:16:16 dun Exp $
 *****************************************************************************
 *  This file is part of the Munge Uid 'N' Gid Emporium (MUNGE).
 *  For details, see <http://www.llnl.gov/linux/munge/>.
 *  UCRL-CODE-2003-???.
 *
 *  Copyright (C) 2003 The Regents of the University of California.
 *  Produced at Lawrence Livermore National Laboratory (cf, DISCLAIMER).
 *  Written by Chris Dunlap <cdunlap@llnl.gov>.
 *
 *  This is free software; you can redistribute it and/or modify it
 *  under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This is distributed in the hope that it will be useful, but WITHOUT
 *  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 *  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 *  for more details.
 *
 *  You should have received a copy of the GNU General Public License;
 *  if not, write to the Free Software Foundation, Inc., 59 Temple Place,
 *  Suite 330, Boston, MA  02111-1307  USA.
 *****************************************************************************/


#if HAVE_CONFIG_H
#  include <config.h>
#endif /* HAVE_CONFIG_H */

#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include "cred.h"
#include "munge_defs.h"


munge_cred_t
cred_create (munge_msg_t m)
{
    munge_cred_t c;

    assert (m != NULL);

    if (!(c = malloc (sizeof (struct munge_cred)))) {
        return (NULL);
    }
    /*  Init ints to 0, chars to \0, ptrs to NULL.
     */
    memset (c, 0, sizeof (*c));

    c->version = MUNGE_CRED_VERSION;
    c->msg = m;
    return (c);
}


void
cred_destroy (munge_cred_t c)
{
    if (!c) {
        return;
    }
    if (c->cred) {
        assert (c->cred_len > 0);
        memset (c->cred, 0, c->cred_len);
        free (c->cred);
    }
    if (c->outer) {
        assert (c->outer_len > 0);
        memset (c->outer, 0, c->outer_len);
        free (c->outer);
    }
    if (c->inner) {
        assert (c->inner_len > 0);
        memset (c->inner, 0, c->inner_len);
        free (c->inner);
    }
    memset (c, 0, sizeof (*c));
    free (c);
    return;
}